from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import UserAccount, EmployeeInformation, AttendanceRecord, LeaveType, LeaveRequest
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import LeaveRequestForm
from django.contrib import messages
from datetime import datetime
from django.db.models import Count, Sum

# Set the timezone to Asia/Manila
PHILIPPINES_TZ = pytz_timezone('Asia/Manila')

@csrf_protect
def index(request):
    if request.method == 'POST':
        username = request.POST.get('email')  # Getting email as username
        password = request.POST.get('password')
        
        try:
            # Try to authenticate using UserAccount
            user = UserAccount.objects.get(username=username)
            stored_password = user.password  # Get the actual stored password
            
            if password == stored_password:  # Compare with actual password
                request.session['user_id'] = str(user.account_id.employee_id)
                request.session['user_role'] = user.role
                request.session['user_name'] = f"{user.account_id.first_name} {user.account_id.last_name}"

                return redirect('home')
            else:
                messages.error(request, f'Invalid password. Format should be: lastname.[A-Z][a-z][0-9][0-9][0-9]')
        except UserAccount.DoesNotExist:
            messages.error(request, 'No account found with this email.')
        
    return render(request, 'pages/index.html')

@csrf_protect
def home(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.session['user_id'])
        context = {
            'employee': employee,
            'user_role': request.session.get('user_role', 'User'),
            'user_name': request.session.get('user_name', '')
        }
        return render(request, 'pages/home.html', context)
    except EmployeeInformation.DoesNotExist:
        return redirect('login')

def custom_admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/admin/")  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "admin/login.html")

def clock_in(request):
    if request.method == 'POST' and 'user_id' in request.session:
        employee_id = request.session['user_id']
        try:
            employee = EmployeeInformation.objects.get(employee_id=employee_id)
            current_time = now().astimezone(PHILIPPINES_TZ)
            attendance, created = AttendanceRecord.objects.get_or_create(
                employee=employee,
                date=current_time.date(),
                defaults={'time_in': current_time.time(), 'status': 'Present'}
            )
            if not created:
                if attendance.time_in is not None:
                    messages.error(request, "You have already clocked in today.")
                else:
                    attendance.time_in = current_time.time()
                    attendance.status = 'Present'
                    attendance.save()
        except EmployeeInformation.DoesNotExist:
            messages.error(request, "Employee not found.")
    return redirect('home')
from django.utils.timezone import now

def clock_out(request):
    if request.method == 'POST' and 'user_id' in request.session:
        employee_id = request.session['user_id']
        try:
            # Retrieve the employee
            employee = EmployeeInformation.objects.get(employee_id=employee_id)
            current_time = now().astimezone(PHILIPPINES_TZ)

            # Find today's attendance record
            try:
                attendance = AttendanceRecord.objects.get(
                    employee=employee,
                    date=current_time.date()
                )

                # Check if the employee has already clocked out
                if attendance.time_out is None:
                    attendance.time_out = current_time.time()  # Set the current time as time_out
                    attendance.status = 'Present'  # Update status if necessary
                    attendance.save()
                    messages.success(request, "Clock-out successful!")
                else:
                    messages.error(request, "You have already clocked out today.")
            except AttendanceRecord.DoesNotExist:
                messages.error(request, "No clock-in record found for today.")
        except EmployeeInformation.DoesNotExist:
            messages.error(request, "Employee not found.")
    else:
        messages.error(request, "Invalid request.")
    return redirect('home')




def calculate_total_hours(time_in, time_out):
    """Calculates the total hours worked based on time_in and time_out"""
    if time_in and time_out:
        time_in = datetime.combine(datetime.today(), time_in)
        time_out = datetime.combine(datetime.today(), time_out)
        total_time = time_out - time_in
        return total_time.seconds / 3600  # Convert seconds to hours
    return 0


from datetime import datetime
from django.shortcuts import render, redirect
from .models import AttendanceRecord, EmployeeInformation

def calculate_working_and_overtime_hours(time_in, time_out, status):
    """Calculates working hours and overtime hours, skipping if status is 'Leave'."""
    if status == 'Leave':
        return 0, 0  # No working or overtime hours for leave days
    
    if time_in and time_out:
        time_in = datetime.combine(datetime.today(), time_in)
        time_out = datetime.combine(datetime.today(), time_out)
        total_time = time_out - time_in
        total_hours = total_time.seconds / 3600  # Convert seconds to hours
        
        # 8 hours workday threshold
        working_hours = min(total_hours, 8)  # Cap working hours at 8
        overtime_hours = max(0, total_hours - 8)  # Overtime is any time beyond 8 hours

        return round(working_hours, 3), round(overtime_hours, 3)
    
    return 0, 0

def attendance_record(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        # Retrieve employee information
        employee = EmployeeInformation.objects.get(employee_id=request.session['user_id'])

        # Retrieve attendance records for the employee
        attendance_records = AttendanceRecord.objects.filter(employee=employee).order_by('-date')

        # Calculate working hours and overtime for each record
        for record in attendance_records:
            record.working_hours, record.overtime_hours = calculate_working_and_overtime_hours(record.time_in, record.time_out, record.status)
            record.save()

        # Calculate the attendance statistics
        
        present_days = attendance_records.filter(status='Present').count()
        absent_days = attendance_records.filter(status='Absent').count()
        leave_days = attendance_records.filter(status='Leave').count()

        # Retrieve the job directly (assuming it's stored as a string or reference in EmployeeInformation)
        job = employee.job  # If job is directly the job name or ID

        # Pass the calculated statistics and job to the context
        context = {
            'attendance_records': attendance_records,
            'user_role': request.session.get('user_role', 'User'),
            'user_name': request.session.get('user_name', ''),
           
            'present_days': present_days,
            'absent_days': absent_days,
            'leave_days': leave_days,  # Add leave days
            'job': job,  # Pass the job to the context
        }

        return render(request, 'pages/attendance_record.html', context)
    
    except EmployeeInformation.DoesNotExist:
        return redirect('login')


from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LeaveType, LeaveRequest
from .forms import LeaveRequestForm

def leave_request_page(request):
    # Check if the user has an associated employee information
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        # Retrieve employee information
        employee = EmployeeInformation.objects.get(employee_id=request.session['user_id'])
    except EmployeeInformation.DoesNotExist:
        messages.error(request, "You don't have employee information linked to your account.")
        return redirect('home')  # Redirect to a different page or an error page

    leave_types = LeaveType.objects.all()  # Fetch all leave types
    leave_requests = LeaveRequest.objects.filter(employee=employee)  # Fetch user's leave requests

    # Handle form submission
    if request.method == "POST":
        leave_type_id = request.POST.get('leave_type')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        reason = request.POST.get('reason')
        description = request.POST.get('description')

        try:
            leave_type = LeaveType.objects.get(leave_type_id=leave_type_id)

            # Convert start_date and end_date from string to datetime.date
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Calculate duration based on the dates
            duration = (end_date - start_date).days

            # Create the leave request
            LeaveRequest.objects.create(
                employee=employee,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                duration=duration,
                reason=reason,
                description=description,
                status='Pending'  # Default status
            )
            messages.success(request, "Leave request submitted successfully!")
        except LeaveType.DoesNotExist:
            messages.error(request, "Invalid leave type selected.")
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
        return redirect('leave_request_page')

    total_count = leave_requests.count()
    approved_count = leave_requests.filter(status='Approved').count()
    pending_count = leave_requests.filter(status='Pending').count()

    context = {
        'leave_types': leave_types,
        'leave_requests': leave_requests,
        'total_count': total_count,
        'approved_count': approved_count,
        'pending_count': pending_count,
    }

    return render(request, 'pages/leave_request.html', context)

from django.shortcuts import render
from django.contrib import messages
from .models import SanctionReport, PerformanceReview

def performance_feedback(request):
    # Fetch all sanction reports from the database, ordered by sanction_date
    sanction_reports = SanctionReport.objects.all().order_by('-sanction_date')

    # Fetch all performance reviews from the database, ordered by review_date
    performance_reviews = PerformanceReview.objects.all().order_by('-review_date')

    # Placeholder for feedback data related to sanction reports
    feedback_data = []  # Replace with actual logic if feedback is implemented

    # Handle POST request for feedback submission (for sanction reports)
    if request.method == 'POST':
        # Fetch the SanctionReport object by the report ID sent in the form
        report_id = request.POST.get('report_id')  # Should be sent in the form
        feedback_text = request.POST.get('feedback')  # Feedback content

        if report_id and feedback_text:
            try:
                # Assuming you have a Feedback model to save feedback for sanction reports
                sanction_report = SanctionReport.objects.get(sanction_id=report_id)
                
                # Create and save feedback object (you'll need to have a feedback model)
                # Example:
                # feedback = Feedback(sanction_report=sanction_report, feedback=feedback_text)
                # feedback.save()

                # For now, we show a success message
                messages.success(request, 'Feedback submitted successfully!')

            except SanctionReport.DoesNotExist:
                messages.error(request, 'Sanction report not found.')

    return render(request, 'pages/performance_feedback.html', {
        'sanction_reports': sanction_reports,
        'performance_reviews': performance_reviews,
        'feedback_data': feedback_data,
    })

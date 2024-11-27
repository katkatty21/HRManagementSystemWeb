from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import UserAccount, EmployeeInformation, AttendanceRecord, LeaveType, LeaveRequest
from django.views.decorators.csrf import csrf_protect

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import LeaveRequest, LeaveType
from .forms import LeaveRequestForm


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




def attendance_record(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        # Retrieve employee information
        employee = EmployeeInformation.objects.get(employee_id=request.session['user_id'])

        # Retrieve attendance records for the employee
        attendance_records = AttendanceRecord.objects.filter(employee=employee).order_by('-date')

        # Calculate the attendance statistics
        total_attendance = attendance_records.count()
        present_days = attendance_records.filter(status='Present').count()
        absent_days = attendance_records.filter(status='Absent').count()

        # Retrieve the job directly (assuming it's stored as a string or reference in EmployeeInformation)
        job = employee.job  # If job is directly the job name or ID

        # Pass the calculated statistics and job to the context
        context = {
            'attendance_records': attendance_records,
            'user_role': request.session.get('user_role', 'User'),
            'user_name': request.session.get('user_name', ''),
            'total_attendance': total_attendance,
            'present_days': present_days,
            'absent_days': absent_days,
            'job': job,  # Pass the job to the context
        }

        return render(request, 'pages/attendance_record.html', context)
    except EmployeeInformation.DoesNotExist:
        return redirect('login')
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LeaveRequestForm
from .models import LeaveType, LeaveRequest, UserAccount
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@login_required
def leave_request_page(request):
    leave_types = LeaveType.objects.all()  # Get all leave types
    try:
        # Find UserAccount for the logged-in user
        user_account = UserAccount.objects.get(username=request.user.email)
        # Get the related EmployeeInformation object
        employee_info = user_account.account_id
        # Fetch leave requests for that employee
        leave_requests = LeaveRequest.objects.filter(employee=employee_info)
    except UserAccount.DoesNotExist:
        leave_requests = []  # If no UserAccount exists for this user, return empty list

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = employee_info  # Set the employee info for the leave request
            leave_request.save()
            return redirect('leave_request_page')
    else:
        form = LeaveRequestForm()

    return render(request, 'pages/leave_request.html', {
        'form': form,
        'leave_requests': leave_requests,
        'leave_types': leave_types,
    })

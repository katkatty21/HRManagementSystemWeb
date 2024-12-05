import datetime
from decimal import Decimal
from django.shortcuts import render
from django.utils.timezone import now, localtime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import EmployeeInformation, AttendanceRecord, LeaveRequest, LeaveType
from hraccount.views import admin_home, user_home
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
from .models import (
    EmployeeSalary, 
    PayrollPeriod, 
    PayrollRecord,
    PayrollCorrectionRequest,
    PayrollAdjustment,
    EmployeeInformation
)
from hraccount.models import UserAccount
from .forms import (
    PayrollPeriodForm,
    PayrollCorrectionRequestForm,
    PayrollAdjustmentForm
)
import csv
from django.utils import timezone

PHILIPPINES_TZ = pytz_timezone('Asia/Manila')

@login_required(login_url='login')
def admin_clock_in(request):
    # Get the employee information using the user's account_id (UUID)
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user.account_id)  # Assuming 'id' is UUID in both User and EmployeeInformation

        current_time = now().astimezone(PHILIPPINES_TZ)  # Ensure PHILIPPINES_TZ is defined in your timezone settings

        # Check if employee has already clocked in today
        existing_record = AttendanceRecord.objects.filter(
            employee=employee,
            date=current_time.date()
        ).first()

        if existing_record:
            if existing_record.time_in and not existing_record.time_out:
                messages.error(request, "You are already clocked in today.")
            else:
                messages.error(request, "You have already clocked out today.")
        else:
            AttendanceRecord.objects.create(
                employee=employee,
                date=current_time.date(),
                time_in=current_time.time(),
                status='Present'
            )
            messages.success(request, "Successfully clocked in.")

    except EmployeeInformation.DoesNotExist:
        messages.error(request, "Employee information not found.")

    return redirect('admin_home')  # Redirect to admin page

def user_clock_in(request):
    # Get the employee information using the user's account_id (UUID)
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user.account_id)  # Assuming 'id' is UUID in both User and EmployeeInformation

        current_time = now().astimezone(PHILIPPINES_TZ)  # Ensure PHILIPPINES_TZ is defined in your timezone settings

        # Check if employee has already clocked in today
        existing_record = AttendanceRecord.objects.filter(
            employee=employee,
            date=current_time.date()
        ).first()

        if existing_record:
            if existing_record.time_in and not existing_record.time_out:
                messages.error(request, "You are already clocked in today.")
            else:
                messages.error(request, "You have already clocked out today.")
        else:
            AttendanceRecord.objects.create(
                employee=employee,
                date=current_time.date(),
                time_in=current_time.time(),
                status='Present'
            )
            messages.success(request, "Successfully clocked in.")

    except EmployeeInformation.DoesNotExist:
        messages.error(request, "Employee information not found.")

    return redirect('user_home')  # Redirect to admin page

@login_required(login_url='login')
def admin_clock_out(request):
    # Get the employee information using the user's account_id (UUID)
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user.account_id)  # Assuming 'id' is UUID in both User and EmployeeInformation

        current_time = now().astimezone(PHILIPPINES_TZ)  # Ensure PHILIPPINES_TZ is defined in your timezone settings

        # Find the clock-in record for today where time_in is set, but time_out is still null
        attendance_record = AttendanceRecord.objects.filter(
            employee=employee,
            date=current_time.date(),
            time_in__isnull=False,
            time_out__isnull=True
        ).first()

        if attendance_record:
            # Update the clock-out time and calculate total hours
            attendance_record.time_out = current_time.time()
            attendance_record.total_hours = attendance_record.calculate_total_hours()
            attendance_record.save()

            messages.success(request, f"Clocked out successfully! Total hours: {attendance_record.total_hours:.2f}")
        else:
            messages.error(request, "No active clock-in record found.")
    
    except EmployeeInformation.DoesNotExist:
        messages.error(request, "Employee not found.")

    return redirect('admin_home')
    
@login_required(login_url='login')
def user_clock_out(request):
    # Get the employee information using the user's account_id (UUID)
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user.account_id)  # Assuming 'id' is UUID in both User and EmployeeInformation

        current_time = now().astimezone(PHILIPPINES_TZ)  # Ensure PHILIPPINES_TZ is defined in your timezone settings

        # Find the clock-in record for today where time_in is set, but time_out is still null
        attendance_record = AttendanceRecord.objects.filter(
            employee=employee,
            date=current_time.date(),
            time_in__isnull=False,
            time_out__isnull=True
        ).first()

        if attendance_record:
            # Update the clock-out time and calculate total hours
            attendance_record.time_out = current_time.time()
            attendance_record.total_hours = attendance_record.calculate_total_hours()
            attendance_record.save()

            messages.success(request, f"Clocked out successfully! Total hours: {attendance_record.total_hours:.2f}")
        else:
            messages.error(request, "No active clock-in record found.")
    
    except EmployeeInformation.DoesNotExist:
        messages.error(request, "Employee not found.")

    return redirect('user_home')

def attendance_record(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.session['user_id'])
        attendance_records = AttendanceRecord.objects.filter(employee=employee).order_by('-date')
        context = {
            'attendance_records': attendance_records,
            'user_role': request.session.get('user_role', 'User'),
            'user_name': request.session.get('user_name', ''),
        }
        return render(request, 'pages/attendance_record.html', context)
    except EmployeeInformation.DoesNotExist:
        return redirect('login')
    
@login_required(login_url='login')
def admin_attendance_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
    attendance_records = AttendanceRecord.objects.all().select_related('employee').order_by('-date')
    return render(request, 'admin/attendance_record.html', {
        'attendance_records': attendance_records
    })

def attendance_record(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.session['user_id'])
        attendance_records = AttendanceRecord.objects.filter(employee=employee).order_by('-date')
        context = {
            'attendance_records': attendance_records,
            'user_role': request.session.get('user_role', 'User'),
            'user_name': request.session.get('user_name', ''),
        }
        return render(request, 'admin/attendance_record.html', context)
    except EmployeeInformation.DoesNotExist:
        return redirect('login')
    
@login_required(login_url='login')
def attendance_list(request):
    attendance_records = AttendanceRecord.objects.all().select_related('employee').order_by('-date')
    return render(request, 'admin/attendance_record.html', {
        'attendance_records': attendance_records
    })



    
@login_required(login_url='login')
def leave_request(request):
    # The user is already logged in, so we can directly use request.user
    try:
        # Retrieve employee information using the user's account_id (assuming account_id is part of the User model)
        employee = EmployeeInformation.objects.get(employee_id=request.user.account_id)
    except EmployeeInformation.DoesNotExist:
        messages.error(request, "You don't have employee information linked to your account.")
        return redirect('user_home')  # Redirect to home or another page if no employee information


    leave_types = LeaveType.objects.all()  # Fetch all leave types
    leave_requests = LeaveRequest.objects.filter(employee=employee)  # Fetch user's leave requests

    # Handle form submission for new leave request
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
        return redirect('leave_request')

    # Get the counts for approved, pending, and rejected statuses, regardless of the filter
    total_count = leave_requests.count()
    approved_count = LeaveRequest.objects.filter(employee=employee, status='Approved').count()
    pending_count = LeaveRequest.objects.filter(employee=employee, status='Pending').count()
    rejected_count = LeaveRequest.objects.filter(employee=employee, status='Rejected').count()

    # Filtering logic
    filter_status = request.GET.get('status', 'all')  # Default to 'all' if no status is selected
    if filter_status != 'all':
        leave_requests = leave_requests.filter(status=filter_status)

    # Sorting logic
    sort_order = request.GET.get('sort', 'latest')  # Default to 'latest' if no sort is selected
    if sort_order == 'latest':
        leave_requests = leave_requests.order_by('-start_date')
    elif sort_order == 'oldest':
        leave_requests = leave_requests.order_by('start_date')

    # Pagination
    paginator = Paginator(leave_requests, 10)  # Show 10 leave requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'leave_types': leave_types,
        'leave_requests': page_obj,
        'total_count': total_count,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'filter_status': filter_status,
        'sort_order': sort_order,
    }

    return render(request, 'user/leave_request.html', context)



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


from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import AttendanceRecord, EmployeeInformation
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def attendance_record(request):
    try:
        # Retrieve employee information using the user's account_id (assuming account_id is part of the User model)
        employee = EmployeeInformation.objects.get(employee_id=request.user.account_id)
    except EmployeeInformation.DoesNotExist:
        messages.error(request, "You don't have employee information linked to your account.")
        return redirect('user_home')  # Redirect to home or another page if no employee information

    # Get filter status from request (default to 'all' if not provided)
    filter_status = request.GET.get('status', 'all')

    # Retrieve all attendance records for the employee (no filtering for counts)
    all_attendance_records = AttendanceRecord.objects.filter(employee=employee).order_by('-date')

    # If a specific status is selected, filter the records
    if filter_status != 'all':
        attendance_records = all_attendance_records.filter(status=filter_status)
    else:
        attendance_records = all_attendance_records

    # Paginate the filtered attendance records
    paginator = Paginator(attendance_records, 5)  # Show 5 records per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object for pagination

    # Calculate working hours and overtime for each record
    for record in page_obj:
        record.working_hours, record.overtime_hours = calculate_working_and_overtime_hours(record.time_in, record.time_out, record.status)
        record.save()

    # Calculate the attendance statistics based on all records (no filter)
    present_days = all_attendance_records.filter(status='Present').count()
    absent_days = all_attendance_records.filter(status='Absent').count()
    leave_days = all_attendance_records.filter(status='Leave').count()

    # Retrieve the job directly (assuming it's stored as a string or reference in EmployeeInformation)
    job = employee.job  # If job is directly the job name or ID

    # Pass the calculated statistics and job to the context
    context = {
        'page_obj': page_obj,
        'user_role': request.session.get('user_role', 'User'),
        'user_name': request.session.get('user_name', ''),
        'present_days': present_days,
        'absent_days': absent_days,
        'leave_days': leave_days,  # Add leave days
        'job': job,  # Pass the job to the context
        'filter_status': filter_status,  # Pass the filter status to the template for persistence
    }

    return render(request, 'user/attendance_record.html', context)





from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SanctionReport, PerformanceReview

@login_required(login_url='login')
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

    return render(request, 'user/performance_feedback.html', {
        'sanction_reports': sanction_reports,
        'performance_reviews': performance_reviews,
        'feedback_data': feedback_data,
    })






from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EmployeeInformation, PeerFeedback


@login_required(login_url='login')
def peer_feedback(request):
    try:
        # Retrieve employee information using the user's account_id (assuming account_id is part of the User model)
        employee = EmployeeInformation.objects.get(employee_id=request.user.account_id)
    except EmployeeInformation.DoesNotExist:
        messages.error(request, "You don't have employee information linked to your account.")
        return redirect('user_home')  # Redirect to home or another page if no employee information
   

    try:
        # Retrieve the logged-in user's employee information using 'user_id' from session
        evaluator = EmployeeInformation.objects.get(employee_id=request.user.account_id)
    except EmployeeInformation.DoesNotExist:
        messages.error(request, f"Employee information not found for user with ID {request.user.account_id}.")
        return redirect('user_home')  # Redirect to the home page or any relevant page
    except Exception as e:
        messages.error(request, f"An unexpected error occurred while fetching employee info: {str(e)}")
        return redirect('user_home')  # Handle any unexpected erro

    try:
        # Fetch employees from the same department as the evaluator and get their names
        employees_to_evaluate = EmployeeInformation.objects.filter(job__department=evaluator.job.department)

        # Get employee IDs that have already been given feedback
        feedback_given_ids = PeerFeedback.objects.filter(from_user=evaluator).values_list('to_user', flat=True)

        # Filter out employees who have already received feedback
        employees_to_evaluate = employees_to_evaluate.exclude(employee_id__in=feedback_given_ids).values('employee_id', 'first_name', 'last_name')
        
    except Exception as e:
        messages.error(request, f"An error occurred while fetching employees to evaluate: {str(e)}")
        return redirect('peer_feedback')  # Return to peer feedback page if there's an issue with fetching employees

    if request.method == 'POST':
        # Get the selected employee to evaluate (from the POST request)
        employee_to_evaluate_id = request.POST.get('employee_to_evaluate')

        if not employee_to_evaluate_id:
            messages.error(request, "No employee selected for evaluation. Please select an employee.")
            return redirect('peer_feedback')  # Redirect back to the peer feedback page if no employee selected

        try:
            # Ensure the employee exists before proceeding
            employee_to_evaluate = EmployeeInformation.objects.filter(employee_id=employee_to_evaluate_id).first()

            if not employee_to_evaluate:
                messages.error(request, f"Selected employee with ID {employee_to_evaluate_id} not found.")
                return redirect('peer_feedback')

            # Create and save the feedback for the selected employee
            feedback = PeerFeedback(
                from_user=evaluator,
                to_user=employee_to_evaluate,  # Save the full EmployeeInformation object, not just the name
                question_1=request.POST.get('question_1'),
                question_2=request.POST.get('question_2'),
                question_3=request.POST.get('question_3'),
                question_4=request.POST.get('question_4'),
                question_5=request.POST.get('question_5'),
                question_6=request.POST.get('question_6')
            )
            feedback.save()

            # Show a success message and re-render the peer feedback page
            messages.success(request, "Feedback submitted successfully!")
            return redirect('peer_feedback')  # Redirect back to the peer feedback page to avoid re-submission

        except Exception as e:
            messages.error(request, f"An error occurred while processing the feedback: {str(e)}")
            return redirect('peer_feedback')  # Return to the page if any error occurs during feedback processing

    # Render the page with the evaluator's information and the list of employees to evaluate
    return render(request, 'user/peer_feedback.html', {
        'evaluator': evaluator,
        'employees_to_evaluate': employees_to_evaluate
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EmployeeInformation, SelfAssessment
from django.utils import timezone

@login_required(login_url='login')
def self_assessment_view(request):
    try:
        # Retrieve employee information using the user's account_id (assuming account_id is part of the User model)
        employee = EmployeeInformation.objects.get(employee_id=request.user.account_id)
    except EmployeeInformation.DoesNotExist:
        messages.error(request, "You don't have employee information linked to your account.")
        return redirect('user_home')  # Redirect to home or another page if no employee information

    # Check if the user has already submitted the self-assessment this month
    current_month = timezone.now().month
    if SelfAssessment.objects.filter(employee=employee, submitted_at__month=current_month).exists():
        messages.error(request, "You have already submitted your self-assessment for this month.")
        return redirect('user_home')  # Redirect or display a message indicating the user can't submit again this month

    if request.method == 'POST':
        performance_rating = request.POST.get('performance_rating')
        skill_development = request.POST.get('skill_development')
        teamwork = request.POST.get('teamwork')
        communication_skills = request.POST.get('communication_skills')
        company_culture = request.POST.get('company_culture')
        work_life_balance = request.POST.get('work_life_balance')
        suggestions_for_improvement = request.POST.get('suggestions_for_improvement')

        # Validate the form
        if not all([performance_rating, skill_development, teamwork, communication_skills, company_culture, work_life_balance, suggestions_for_improvement]):
            messages.error(request, "All fields are required.")
            return render(request, 'user/self_assessment.html', {'employee': employee})

        # Save the self-assessment data
        SelfAssessment.objects.create(
            employee=employee,
            performance_rating=performance_rating,
            skill_development=skill_development,
            teamwork=teamwork,
            communication_skills=communication_skills,
            company_culture=company_culture,
            work_life_balance=work_life_balance,
            suggestions_for_improvement=suggestions_for_improvement,
        )
        messages.success(request, "Your self-assessment has been submitted successfully.")
        return redirect('user_home')

    return render(request, 'user/self_assessment.html', {'employee': employee})




from .models import LeaveRequest


@login_required(login_url='login')
def leave_list(request):
    # Handle status update
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        new_status = request.POST.get('status')
        try:
            leave_request = LeaveRequest.objects.get(leave_id=leave_id)
            leave_request.status = new_status
            leave_request.save()
            messages.success(request, f"Status for leave request {leave_id} updated successfully.")
        except LeaveRequest.DoesNotExist:
            messages.error(request, "Leave request not found.")
    
    # Fetch all leave requests
    leave_requests = LeaveRequest.objects.select_related('employee', 'leave_type').order_by('-start_date')
    context = {
        'leave_requests': leave_requests,
    }
    return render(request, 'admin/admin_leave.html', context)


from django.shortcuts import render
from .models import SanctionReport, SelfAssessment, PeerFeedback, PerformanceReview

def performance_management(request):
    filter_type = request.GET.get('filter', '')
    headers, records = [], []

    if filter_type == 'sanction_reports':
        headers = ['Sanction ID', 'Employee', 'Sanction Type', 'Sanction Date', 'Status', 'Actions']
        records = SanctionReport.objects.all().values(
            'sanction_id', 'employee__first_name', 'sanction_type', 'sanction_date', 'status'
        )
    elif filter_type == 'self_assessment':
        headers = ['Assessment ID', 'Employee', 'Performance Rating', 'Skill Development', 'Teamwork',
                   'Communication Skills', 'Company Culture', 'Work-Life Balance', 'Submitted At']
        records = SelfAssessment.objects.all().values(
            'self_assessment_id', 'employee__first_name', 'performance_rating', 'skill_development',
            'teamwork', 'communication_skills', 'company_culture', 'work_life_balance', 'submitted_at'
        )
    elif filter_type == 'peer_feedback':
        headers = ['Feedback ID', 'From User', 'To User', 'Created At']
        records = PeerFeedback.objects.all().values(
            'feedback_id', 'from_user__first_name', 'to_user__first_name', 'created_at'
        )
    elif filter_type == 'supervisor_feedback':
        headers = ['Review ID', 'Employee', 'Review Date', 'Reviewer', 'Performance Score']
        records = PerformanceReview.objects.all().values(
            'review_id', 'employee__first_name', 'review_date', 'reviewer__first_name', 'performance_score'
        )
    else:
        headers = ['Record Type', 'Details']  # Default view
        records = []  # Handle no filter or default case

    return render(request, 'admin/admin_performance_management.html', {
        'headers': headers,
        'records': records,
        'filter': filter_type,
    })

from django.shortcuts import get_object_or_404, redirect

def update_status(request, sanction_id):
    if request.method == 'POST':
        sanction = get_object_or_404(SanctionReport, sanction_id=sanction_id)
        sanction.status = request.POST.get('status')
        sanction.save()
        return redirect('performance_management')


# Admin Views
@login_required(login_url='login')
def manage_payroll_period(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        period_type = request.POST.get('period_type')
        
        PayrollPeriod.objects.create(
            start_date=start_date,
            end_date=end_date,
            period_type=period_type
        )
        messages.success(request, 'Payroll period created successfully.')
        return redirect('payroll_periods')
    
    periods = PayrollPeriod.objects.all().order_by('-start_date')
    return render(request, 'admin/payroll_periods.html', {'periods': periods})

@login_required(login_url='login')
def manage_employee_salary(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        pay_type = request.POST.get('pay_type')
        base_salary = request.POST.get('base_salary')
        effective_date = request.POST.get('effective_date')
        
        try:
            employee = EmployeeInformation.objects.get(employee_id__account_id=employee_id)
            
            EmployeeSalary.objects.update_or_create(
                employee=employee,
                defaults={
                    'pay_type': pay_type,
                    'base_salary': base_salary,
                    'effective_date': effective_date
                }
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Employee salary updated successfully'
                })
            
            messages.success(request, 'Employee salary updated successfully')
            return redirect('employee_salaries')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=400)
            
            messages.error(request, f'Error: {str(e)}')
            return redirect('employee_salaries')
    
    # Get all employees (excluding admins)
    employees = EmployeeInformation.objects.select_related('employee_id').filter(
        employee_id__role='User'
    ).exclude(employee_id__role='Admin')
    
    # Get all salaries
    salaries = EmployeeSalary.objects.select_related('employee').all()
    
    return render(request, 'admin/employee_salaries.html', {
        'employees': employees,
        'salaries': salaries
    })

@login_required(login_url='login')
def manage_payroll_adjustment(request):
    adjustments = PayrollAdjustment.objects.all().order_by('-date_added')
    form = PayrollAdjustmentForm()
    
    if request.method == 'POST':
        adjustment_id = request.GET.get('id')
        action = request.POST.get('action')
        
        if action == 'delete' and adjustment_id:
            adjustment = get_object_or_404(PayrollAdjustment, id=adjustment_id)
            adjustment.delete()
            messages.success(request, 'Payroll adjustment deleted successfully.')
            return redirect('payroll_adjustments')
            
        if adjustment_id:
            adjustment = get_object_or_404(PayrollAdjustment, id=adjustment_id)
            form = PayrollAdjustmentForm(request.POST, instance=adjustment)
        else:
            form = PayrollAdjustmentForm(request.POST)
            
        if form.is_valid():
            form.save()
            messages.success(request, 'Payroll adjustment saved successfully.')
            return redirect('payroll_adjustments')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    context = {
        'adjustments': adjustments,
        'form': form
    }
    return render(request, 'admin/payroll_adjustments.html', context)

@login_required(login_url='login')
def process_payroll(request, period_id):
    period = get_object_or_404(PayrollPeriod, uuid=period_id)
    
    if request.method == 'POST':
        if not period.is_processed:
            employees = EmployeeInformation.objects.filter(is_active=True)
            
            for employee in employees:
                try:
                    salary = EmployeeSalary.objects.get(employee=employee)
                    
                    # Calculate bonuses and deductions
                    bonuses = PayrollAdjustment.objects.filter(
                        employee=employee,
                        payroll_period=period,
                        adjustment_type='BONUS'
                    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
                    
                    deductions = PayrollAdjustment.objects.filter(
                        employee=employee,
                        payroll_period=period,
                        adjustment_type='DEDUCTION'
                    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
                    
                    # Calculate net salary
                    net_salary = salary.base_salary + bonuses - deductions
                    
                    # Create payroll record
                    PayrollRecord.objects.create(
                        employee=employee,
                        payroll_period=period,
                        base_salary=salary.base_salary,
                        total_bonus=bonuses,
                        total_deduction=deductions,
                        net_salary=net_salary,
                        is_finalized=True
                    )
                except EmployeeSalary.DoesNotExist:
                    messages.warning(request, f'No salary information found for {employee.get_full_name()}')
                    continue
            
            period.is_processed = True
            period.save()
            messages.success(request, 'Payroll processed successfully.')
            return redirect('payroll_periods')
    
    context = {
        'period': period,
    }
    return render(request, 'admin/process_payroll.html', context)

@login_required(login_url='login')
def export_payroll(request, period_id):
    period = get_object_or_404(PayrollPeriod, uuid=period_id)
    records = PayrollRecord.objects.filter(payroll_period=period)
    
    export_format = request.GET.get('format', 'pdf')
    
    if export_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="payroll_{period.start_date}_{period.end_date}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Employee', 'Base Salary', 'Total Bonus', 'Total Deduction', 'Net Salary'])
        
        for record in records:
            writer.writerow([
                f"{record.employee.first_name} {record.employee.last_name}",
                record.base_salary,
                record.total_bonus,
                record.total_deduction,
                record.net_salary
            ])
        
        return response
    else:  # PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="payroll_{period.start_date}_{period.end_date}.pdf"'
        
        # Create the PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            alignment=1,  # Center alignment
            spaceAfter=30
        )
        
        # Add title
        elements.append(Paragraph('Payroll Report', title_style))
        elements.append(Paragraph(f'Period: {period.period_type}', styles['Normal']))
        elements.append(Paragraph(f'Date Range: {period.start_date} to {period.end_date}', styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Create table data
        data = [['Employee', 'Base Salary', 'Total Bonus', 'Total Deduction', 'Net Salary']]
        for record in records:
            data.append([
                f"{record.employee.first_name} {record.employee.last_name}",
                str(record.base_salary),
                str(record.total_bonus),
                str(record.total_deduction),
                str(record.net_salary)
            ])
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        return response

@login_required(login_url='login')
def manage_correction_requests(request):
    correction_requests = PayrollCorrectionRequest.objects.select_related(
        'employee', 'payroll_record'
    ).order_by('-date_submitted')
    return render(request, 'admin/correction_requests.html', {
        'correction_requests': correction_requests
    })

@login_required(login_url='login')
def approve_correction_request(request, request_id):
    correction_request = get_object_or_404(PayrollCorrectionRequest, id=request_id)
    correction_request.status = 'APPROVED'
    correction_request.processed_at = timezone.now()
    correction_request.processed_by = request.user
    correction_request.save()
    messages.success(request, 'Correction request approved successfully.')
    return redirect('correction_requests')

@login_required(login_url='login')
def reject_correction_request(request, request_id):
    correction_request = get_object_or_404(PayrollCorrectionRequest, id=request_id)
    correction_request.status = 'REJECTED'
    correction_request.processed_at = timezone.now()
    correction_request.processed_by = request.user
    correction_request.save()
    messages.success(request, 'Correction request rejected successfully.')
    return redirect('correction_requests')

@login_required(login_url='login')
def view_payroll(request):
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user)
        records = PayrollRecord.objects.filter(employee=employee).order_by('-payroll_period__start_date')
        return render(request, 'employee/view_payroll.html', {
            'records': records
        })
    except EmployeeInformation.DoesNotExist:
        messages.error(request, 'Employee information not found.')
        return redirect('user_home')

@login_required(login_url='login')
def view_payroll_detail(request, record_id):
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user)
        record = get_object_or_404(PayrollRecord, id=record_id, employee=employee)
        return render(request, 'employee/view_payroll_detail.html', {
            'record': record
        })
    except EmployeeInformation.DoesNotExist:
        messages.error(request, 'Employee information not found.')
        return redirect('hraccount:user_home')

@login_required(login_url='login')
def submit_correction_request(request):
    if request.method == 'POST':
        try:
            employee = EmployeeInformation.objects.get(employee_id=request.user)
            record_id = request.POST.get('record_id')
            description = request.POST.get('description')
            
            record = get_object_or_404(PayrollRecord, id=record_id, employee=employee)
            
            PayrollCorrectionRequest.objects.create(
                employee=employee,
                payroll_record=record,
                description=description
            )
            
            messages.success(request, 'Correction request submitted successfully.')
            return redirect('view_payroll')
            
        except Exception as e:
            messages.error(request, f'Error submitting correction request: {str(e)}')
            return redirect('view_payroll')
    
    return redirect('view_payroll')

@login_required(login_url='login')
def download_payslip(request, record_id):
    try:
        employee = EmployeeInformation.objects.get(employee_id=request.user)
        record = get_object_or_404(PayrollRecord, id=record_id, employee=employee)
        
        # Create the HttpResponse object with PDF headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="payslip_{record.payroll_period.start_date.strftime("%Y%m")}.pdf"'
        
        # Create the PDF object using reportlab
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        # Add title
        elements.append(Paragraph("PAYSLIP", title_style))
        elements.append(Spacer(1, 12))
        
        # Add employee information
        data = [
            ['Employee Information', ''],
            ['Name:', f"{record.employee.first_name} {record.employee.last_name}"],
            ['Department:', str(record.employee.job.department.department_name)],
            ['Position:', str(record.employee.job.job_title)],
            ['Pay Period:', f"{record.payroll_period.start_date.strftime('%B %d, %Y')} - {record.payroll_period.end_date.strftime('%B %d, %Y')}"],
            ['', ''],
            ['Earnings', ''],
            ['Base Salary:', f"P{record.base_salary:,.2f}"],
            ['Total Bonus:', f"P{record.total_bonus:,.2f}"],
            ['Total Deduction:', f"P{record.total_deduction:,.2f}"],
            ['Net Pay:', f"P{record.net_salary:,.2f}"],
        ]
        
        # Create table
        table = Table(data, colWidths=[4*inch, 3*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.grey),
            ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),  # Earnings header
            ('TEXTCOLOR', (0, 6), (-1, 6), colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),  # Line above total
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Make total bold
        ]))
        elements.append(table)
        
        # Add adjustments details
        adjustments = PayrollAdjustment.objects.filter(
            employee=record.employee,
            payroll_period=record.payroll_period
        )
        if adjustments:
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Adjustments", styles['Heading2']))
            data = []
            for adj in adjustments:
                data.append([adj.get_adjustment_type_display(), adj.description, f"P{adj.amount:,.2f}"])
            table = Table(data, colWidths=[2*inch, 3*inch, 2*inch])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.grey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer and write it to the response
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
        
    except EmployeeInformation.DoesNotExist:
        messages.error(request, 'Employee information not found.')
        return redirect('user_home')


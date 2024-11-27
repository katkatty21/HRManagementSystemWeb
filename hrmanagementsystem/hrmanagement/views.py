from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import UserAccount, EmployeeInformation, AttendanceRecord, Department, Job
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required


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
        
        # Check if employee is clocked in today
        today = timezone.now().date()
        is_clocked_in = AttendanceRecord.objects.filter(
            employee=employee,
            date=today,
            time_in__isnull=False,
            time_out__isnull=True
        ).exists()
        
        context = {
            'employee': employee,
            'user_role': request.session.get('user_role', 'User'),
            'user_name': request.session.get('user_name', ''),
            'is_clocked_in': is_clocked_in
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

            # Check if employee has already clocked in today
            existing_record = AttendanceRecord.objects.filter(
                employee=employee,
                date=current_time.date(),
                time_in__isnull=False
            ).first()

            if existing_record:
                messages.error(request, "You have already clocked in today.")
            else:
                AttendanceRecord.objects.create(
                    employee=employee,
                    date=current_time.date(),
                    time_in=current_time.time(),
                    status='Present'
                )
                messages.success(request, "Successfully clocked in.")
                
        except EmployeeInformation.DoesNotExist:
            messages.error(request, "Employee not found.")

    return redirect('home')

def clock_out(request):
    if request.method == 'POST' and 'user_id' in request.session:
        employee_id = request.session['user_id']
        try:
            employee = EmployeeInformation.objects.get(employee_id=employee_id)
            current_time = localtime()
            
            # Fetch today's attendance record
            attendance_record = AttendanceRecord.objects.filter(
                employee=employee,
                date=current_time.date(),
                time_in__isnull=False,
                time_out__isnull=True
            ).first()

            if attendance_record:
                attendance_record.time_out = current_time.time()
                attendance_record.total_hours = attendance_record.calculate_total_hours()
                attendance_record.save()

                messages.success(request, "Successfully clocked out.")
            else:
                messages.error(request, "No active clock-in record found.")
        except EmployeeInformation.DoesNotExist:
            messages.error(request, "Employee not found.")

    return redirect('home')


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
    
def user_profile(request):
    """
    Displays the profile of the logged-in user.
    """
    if 'user_id' not in request.session:
        return redirect('login')
    
    employee = get_object_or_404(EmployeeInformation, employee_id=request.session['user_id'])
    context = {
        'employee': employee,
        'user_role': request.session.get('user_role', 'User'),
        'user_name': request.session.get('user_name', '')
    }
    return render(request, 'pages/userprofile.html', context)

@login_required
def update_profile(request):
    """
    Allows the logged-in user to update their profile information.
    Excludes job, employment_status, employee_id, date_hired, and role.
    """
    if 'user_id' not in request.session:
        return redirect('login')

    employee = get_object_or_404(EmployeeInformation, employee_id=request.session['user_id'])

    if request.method == 'POST':
        # Updating editable fields only
        employee.first_name = request.POST.get('first_name')
        employee.middle_name = request.POST.get('middle_name')  # Optional, may be blank
        employee.last_name = request.POST.get('last_name')
        employee.birthdate = request.POST.get('birthdate')
        employee.sex = request.POST.get('sex')
        employee.marital_status = request.POST.get('marital_status')
        employee.nationality = request.POST.get('nationality')
        employee.address = request.POST.get('address')
        employee.city = request.POST.get('city')
        employee.province = request.POST.get('province')
        employee.zip_code = request.POST.get('zip_code')
        employee.active_phone_number = request.POST.get('active_phone_number')
        employee.email = request.POST.get('email')
        employee.emergency_contact_name = request.POST.get('emergency_contact_name')
        employee.emergency_contact_rs = request.POST.get('emergency_contact_rs')
        employee.emergency_contact_number = request.POST.get('emergency_contact_number')

        # Update email in UserAccount
        user_account = get_object_or_404(UserAccount, account_id=employee)
        user_account.username = employee.email

        # Save both models
        employee.save()
        user_account.save()

        messages.success(request, "Your profile has been updated successfully!")
        return redirect('userprofile')

    # Render the update form
    context = {
        'employee': employee,
        'sex_choices': EmployeeInformation.SEX_CHOICES,
        'marital_status_choices': EmployeeInformation.MARITAL_STATUS_CHOICES,
    }
    return render(request, 'pages/update_profile.html', context)
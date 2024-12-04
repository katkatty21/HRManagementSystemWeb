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
from .models import EmployeeInformation, AttendanceRecord
from hraccount.views import admin_home, user_home

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

@login_required(login_url='login')
def user_attendance_list(request):
    employee = EmployeeInformation.objects.get(employee_id=request.user.account_id)
    attendance_records = AttendanceRecord.objects.filter(employee=employee).order_by('-date')
    
    return render(request, 'user/attendance_record.html', {
        'attendance_records': attendance_records
    })
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import UserAccount, EmployeeInformation, AttendanceRecord
from django.views.decorators.csrf import csrf_protect


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
            # Get current time in the Philippines time zone
            current_time = now().astimezone(PHILIPPINES_TZ)
            attendance, created = AttendanceRecord.objects.get_or_create(
                employee=employee,
                date=current_time.date(),
                defaults={'time_in': current_time.time()}  # Save time in the correct time zone
            )
            if not created and attendance.time_in is not None:
                messages.error(request, "You have already clocked in today.")
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
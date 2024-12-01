import string, random
from django.core.mail import send_mail
from hraccount.models import UserAccount
from django.http import HttpResponseForbidden
from django.utils.timezone import now, localtime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserAccount
from django.template.loader import render_to_string



def index(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate with email as the username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Check if the user is active
            if user.is_active:
                login(request, user)  # Logs the user in
                # Redirect user based on role and staff status
                if user.is_staff:
                    return redirect('admin_home')  # Admin home page
                else:
                    return redirect('user_home')  # Regular user home page
            else:
                messages.error(request, "Your account is not active. Please contact support.")
                return redirect('login')  # Stay on login page if account is inactive
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
            return redirect('login')  # Stay on the login page if authentication fails

    return render(request, 'index.html')

@login_required(login_url='login')
def admin_home(request):
    # This is the admin home page
    if request.user.role == 'Admin':
        return render(request, 'admin/home.html')
    else:
        return redirect('user_home')  # Redirect non-admins to user home

@login_required(login_url='login')
def user_home(request):
    # This is the user home page
    if request.user.role == 'User':
        return render(request, 'user/home.html')
    else:
        return redirect('admin_home')  # Redirect admins to admin home
    
@login_required(login_url='login')
def users_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    # Fetch the list of users from the UserAccount model
    users = UserAccount.objects.all()
    return render(request, 'admin/users.html', {'users': users})

def generate_password():
    characters = string.ascii_letters + string.digits  # Aa-Zz and 0-9
    password = ''.join(random.choice(characters) for _ in range(5))  # First 5 chars
    password += '-' + ''.join(random.choice(string.digits) for _ in range(4))  # Last 4 digits
    return password

@login_required(login_url='login')
def add_user(request):
    # Generate the password immediately when the page loads
    generated_password = generate_password()

    if request.method == 'POST':
        email = request.POST['email']
        role = request.POST.get('role')  # 'Admin' or 'User'
        is_staff = True if role == 'Admin' else False
        is_superuser = True if role == 'Admin' else False  

        # Create the UserAccount object
        user = UserAccount.objects.create_user(
            username=email,  # Using email as username
            email=email,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        # Set the password for the user (this will hash the password)
        user.set_password(generated_password)  # Hash the password for secure storage
        user.save()

        # Render email message based on the role
        if role == 'Admin':
            subject = 'Welcome to SRK Admin'
            email_body = render_to_string('emails/admin_welcome.html', {
                'user': user,
                'generated_password': generated_password,
                'logo_url': request.build_absolute_uri('/static/logo.svg')
            })
        else:
            subject = 'Welcome to SRK Solutions'
            email_body = render_to_string('emails/user_welcome.html', {
                'user': user,
                'generated_password': generated_password,
                'logo_url': request.build_absolute_uri('/static/logo.svg')
            })

        # Send email with HTML content
        send_mail(
            subject,
            email_body,
            'admin@yourdomain.com',  # Replace with your actual email
            [email],
            fail_silently=False,
            html_message=email_body  # Send HTML content
        )

        # Success message
        messages.success(request, 'User created successfully!')

        # Redirect to the users list page after successful creation
        return redirect('users_list')  # Redirect to users list after success

    # If the form is not submitted yet, render the page with the generated password
    return render(request, 'admin/add_user.html', {'password': generated_password})


@login_required(login_url='login')
def edit_user(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to edit users.")
    
    # Get the user by account_id (UUID)
    user = get_object_or_404(UserAccount, account_id=user_id)
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        # Update user details
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.role = role
        
        # Change is_staff based on the new role
        user.is_staff = True if role == 'Admin' else False
        user.is_superuser = True if role == 'Admin' else False

        
        
        # Save the updated user object
        user.save()
        
        # Provide feedback to the admin
        messages.success(request, "User updated successfully!")
        
        return redirect('users_list')  # Redirect to the users list page
    
    return render(request, 'admin/edit_user.html', {'user': user})

@login_required(login_url='login')
def delete_user(request, user_id):
    # Check if the logged-in user is an admin
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to delete users.")
    
    # Ensure user_id is treated as a UUID and get the user to be deleted
    user = get_object_or_404(UserAccount, account_id=user_id)

    # Check if the logged-in user is deleting their own account
    if request.user == user:
        # If it's the logged-in user, delete the account and log them out
        logout(request)  # Log out the user after deletion
        user.delete()  # Delete the user
        messages.success(request, "Your account has been deleted successfully!")
        return redirect('login')  # Redirect to the login page after deleting own account

    # If it's another user's account, proceed with normal deletion
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('users_list') 


def logout_view(request):
    # Logging out the user and redirecting to login page
    logout(request)
    return redirect('login')  # Adjust the 'login' URL if needed


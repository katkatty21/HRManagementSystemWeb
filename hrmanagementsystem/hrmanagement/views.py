from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

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
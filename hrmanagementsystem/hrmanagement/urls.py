from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'), 
    path('home/', views.home, name='home'), 
    path('clock-in/', views.clock_in, name='clock_in'),
    path('clock-out/', views.clock_out, name='clock_out'),
    path('profile/', views.user_profile, name='userprofile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('attendance-record/', views.attendance_record, name='attendance_record'), 
    path('admin/login/', views.custom_admin_login, name='admin_login'),
]

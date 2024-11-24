from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'), 
    path('home/', views.home, name='home'), 
    path('clock-in/', views.clock_in, name='clock_in'),
    path('attendance-record/', views.attendance_record, name='attendance_record'), 
    path('admin/login/', views.custom_admin_login, name='admin_login'),
]

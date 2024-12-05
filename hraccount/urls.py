from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('hr/admin/home/', views.admin_home, name='admin_home'),
    path('hr/logout/', views.logout_view, name='logout'),
    path('hr/admin/users/', views.users_list, name='users_list'),
    path('hr/admin/add-user/', views.add_user, name='add_user'),
    path('hr/admin/edit-user/<uuid:user_id>/', views.edit_user, name='edit_user'),
    path('hr/admin/delete-user/<uuid:user_id>/', views.delete_user, name='delete_user'),
    path('hr/admin/departments/', views.department_list, name='department_list'),
    path('hr/admin/departments/add/', views.add_department, name='add_department'),
    path('hr/admin/departments/edit/<uuid:department_id>/', views.edit_department, name='edit_department'),
    path('hr/admin/departments/delete/<uuid:department_id>/', views.delete_department, name='delete_department'),
    path('hr/admin/add_job/', views.add_job, name='add_job'),
    path('hr/admin/jobs/', views.jobs, name='jobs'),
    path('hr/admin/edit_job/<uuid:job_id>/', views.edit_job, name='edit_job'),
    path('hr/admin/delete_job/<uuid:job_id>/', views.delete_job, name='delete_job'),
    path('hr/admin/employees/', views.employee_list, name='employee_list'),
    path('hr/admin/employees/add/', views.add_employee, name='add_employee'),
    path('hr/admin/employees/edit/<uuid:employee_id>/', views.edit_employee, name='edit_employee'),
    path('hr/admin/employees/delete/<uuid:employee_id>/', views.delete_employee, name='delete_employee'),
    
    path('hr/user/home/', views.user_home, name='user_home'),
    path('hrmanagement/', include('hrmanagement.urls')),
]

from django.contrib import admin
from .models import Department, Job, EmployeeInformation, UserAccount

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name',)
    list_display_links = ('department_name',)
    search_fields = ('department_name',)
    ordering = ('department_name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('department', 'job_title', 'salary_min', 'salary_max')
    list_display_links = ('job_title',)
    search_fields = ('job_title', 'department__department_name')
    list_filter = ('department',)
    ordering = ('job_title',)

@admin.register(EmployeeInformation)
class EmployeeInformationAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'sex', 'address', 
        'city', 'province', 'zip_code', 'job', 'date_hired'
    )
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'email', 'job__job_title')
    list_filter = ('sex', 'marital_status', 'employment_status', 'role')  # Corrected 'gender' to 'sex'
    ordering = ('last_name', 'first_name')

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')
    list_display_links = ('username',)
    search_fields = ('username', 'account_id__first_name', 'account_id__last_name')
    list_filter = ('role',)
    ordering = ('username',)

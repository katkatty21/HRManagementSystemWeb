from django.contrib import admin
from .models import UserAccount, Department, Job, EmployeeInformation

# Admin for UserAccount
@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'username', 'email', 'first_name', 'last_name', 'role', 'date_account_added')  # Columns to display
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role')  # Searchable fields
    list_filter = ('role', 'date_account_added')  # Filterable fields
    ordering = ('date_account_added',)  # Default ordering
    #exclude = ('account_id',)  # Exclude account_id from forms

# Admin for Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name',)  # Columns to display
    search_fields = ('department_name',)  # Searchable fields

# Admin for Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'department', 'salary_min', 'salary_max')  # Columns to display
    search_fields = ('job_title', 'department__department_name')  # Searchable fields
    list_filter = ('department',)  # Filterable fields
    ordering = ('job_title',)  # Default ordering
    exclude = ('job_id',)  # Exclude job_id from forms

# Admin for EmployeeInformation
@admin.register(EmployeeInformation)
class EmployeeInformationAdmin(admin.ModelAdmin):
    list_display = (
        'profile_picture',
        'first_name', 
        'last_name', 
        'email', 
        'sex', 
        'marital_status', 
        'nationality', 
        'city', 
        'employment_status', 
        'role', 
        'job'
        
    )  # Columns to display
    search_fields = (
        'first_name', 
        'last_name', 
        'email', 
        'nationality', 
        'city', 
        'employment_status', 
        'job__job_title'
    )  # Searchable fields
    list_filter = ('sex', 'marital_status', 'role', 'job')  # Filterable fields
    ordering = ('last_name', 'first_name')  # Default ordering
    #exclude = ('employee_id', 'profile_picture')  # Exclude fields from forms
    list_display_links = ('first_name',)

    readonly_fields = ('email',) 

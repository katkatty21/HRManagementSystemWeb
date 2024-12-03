from django.contrib import admin
from .models import UserAccount, Department, Job, EmployeeInformation
from django.contrib import admin
from django.utils.html import mark_safe

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
    list_display = ('job_title', 'department', 'salary_range','job_description', 'requirements', 'status' )  # Columns to display
    search_fields = ('job_title', 'department__department_name')  # Searchable fields
    list_filter = ('department',)  # Filterable fields
    ordering = ('job_title',)  # Default ordering
    exclude = ('job_id',)  # Exclude job_id from forms



# EmployeeInformation Admin
@admin.register(EmployeeInformation)
class EmployeeInformationAdmin(admin.ModelAdmin):
    list_display = (
        'profile_picture_preview',  # Added profile picture preview
        'first_name', 
        'last_name', 
        'email', 
        'sex', 
        'marital_status', 
        'nationality', 
        'city', 
        'employment_status', 
        'job'
    ) 
    search_fields = (
        'first_name', 
        'last_name', 
        'email', 
        'nationality', 
        'city', 
        'employment_status', 
        'job__job_title'
    )  # Searchable fields
    list_filter = ('sex', 'marital_status', 'job')  # Filterable fields
    ordering = ('last_name', 'first_name')  # Default ordering
    list_display_links = ('first_name',)  # Make 'first_name' clickable to access the detail view
    readonly_fields = ('email',)  # Readonly email field (derived from UserAccount)

    # Method to display profile picture preview
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" alt="Profile Picture" width="50px" height="50px" />')
        return "No Image"
    profile_picture_preview.short_description = 'Profile Picture'  # Custom label for the column

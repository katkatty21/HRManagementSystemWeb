from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.utils.html import format_html
from .models import (
    Department, Job, EmployeeInformation, UserAccount, 
    AttendanceRecord, EmployeePayroll, LeaveRequest, LeaveType,
    JobOpening, Applicant, PerformanceReport, PerformanceReview,
    SanctionReport, Trainings
)

class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'

class MyAdminSite(admin.AdminSite):
    site_header = 'HR Management System'
    login_template = 'admin/login.html'
    
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request, app_label)
        
        for app_label, app_config in app_dict.items():
            if app_label == "hrmanagement":  # Your app label
                # Custom ordering for your models with UserAccount first
                model_order = [
                    # User Management
                    "useraccounts",
                    # Employee Management
                    "employeeinformation",
                    "departments",
                    # Job Management
                    "jobs",
                    "jobopenings",
                    "applicants",
                    # Attendance & Leave
                    "attendancerecord",
                    "leavetype",
                    "leaverequest",
                    # Payroll
                    "employeepayroll",
                    # Performance & Training
                    "performancereport",
                    "performancereview",
                    "sanctionreport",
                    "trainings",
                ]
                
                app_config['models'].sort(
                    key=lambda x: model_order.index(x['object_name'].lower())
                    if x['object_name'].lower() in model_order
                    else len(model_order)
                )
                
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list

admin.site.__class__ = MyAdminSite

# Register UserAccount first
from django.contrib import admin
from django.utils.html import format_html

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_employee_name', 'role', 'date_account_added', 'display_password')
    list_display_links = ('username',)
    search_fields = ('username', 'account_id__first_name', 'account_id__last_name')
    list_filter = ('role', 'date_account_added')
    readonly_fields = ('username', 'password')  # Make username readonly since it's tied to email
    ordering = ('username',)

    def get_employee_name(self, obj):
        """Display the employee's full name"""
        return f"{obj.account_id.first_name} {obj.account_id.last_name}"
    get_employee_name.short_description = 'Employee Name'

    def display_password(self, obj):
        """Display password with copy button"""
        return format_html(
            '<div style="display: flex; align-items: center;">'
            '<span style="margin-right: 10px;">{}</span>'
            '<button type="button" onclick="copyPassword(this)" '
            'data-password="{}" style="padding: 2px 8px; border: 1px solid #ccc; '
            'border-radius: 3px; background: #f0f0f0; cursor: pointer">'
            'Copy</button></div>'
            '<script>'
            'function copyPassword(button) {{'
            '    navigator.clipboard.writeText(button.getAttribute("data-password"));'
            '    button.textContent = "Copied!";'
            '    setTimeout(() => button.textContent = "Copy", 2000);'
            '}}'
            '</script>',
            obj.password,
            obj.password
        )
    display_password.short_description = 'Password'
    display_password.allow_tags = True

    def has_add_permission(self, request):
        return False  # Disable manual adding since accounts are created automatically

    def has_change_permission(self, request, obj=None):
        return True  # Allow changing other fields but username will be readonly
    
@admin.register(EmployeeInformation)
class EmployeeInformationAdmin(admin.ModelAdmin):
    list_display = ('profile_preview', 'first_name', 'last_name', 'sex', 'address', 'city', 'province', 'zip_code', 'job', 'date_hired')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'email', 'job__job_title')
    list_filter = ('sex', 'marital_status', 'employment_status', 'role')
    ordering = ('last_name', 'first_name')
    readonly_fields = ("profile_preview",)

# Rest of your model registrations remain the same
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

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('job_opening_id', 'job', 'department', 'posting_date', 'application_deadline', 'closing_date')
    list_display_links = ('job_opening_id', 'job')
    search_fields = ('job__job_title', 'department__department_name', 'job_opening_id')
    list_filter = ('department', 'posting_date')
    ordering = ('posting_date',)

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('applicant_id', 'job_opening', 'first_name', 'last_name', 'email', 'phone', 'resume_preview', 'applicant_status')
    list_display_links = ('applicant_id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'email', 'job_opening__job__job_title')
    list_filter = ('applicant_status', 'job_opening')
    ordering = ('first_name', 'last_name')
    readonly_fields = ('resume_preview',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('attendance_id', 'employee', 'date', 'time_in', 'time_out', 'total_hours', 'status')
    list_display_links = ('attendance_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'date')
    list_filter = ('status', 'date')
    ordering = ('date',)

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('leave_name', 'max_days_allowed')
    list_display_links = ('leave_name',)
    search_fields = ('leave_name',)
    ordering = ('leave_name',)

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('leave_id', 'employee', 'leave_type', 'start_date', 'end_date', 'duration', 'status')
    list_display_links = ('leave_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'leave_type__leave_name')
    list_filter = ('status', 'leave_type')
    ordering = ('start_date',)

@admin.register(EmployeePayroll)
class EmployeePayrollAdmin(admin.ModelAdmin):
    list_display = ('payroll_id', 'employee', 'pay_period_start', 'pay_period_end', 'gross_salary', 'net_salary', 'hours_worked', 'overtime_hours')
    list_display_links = ('payroll_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'payroll_id')
    list_filter = ('pay_period_start', 'pay_period_end')
    ordering = ('pay_period_start',)

@admin.register(PerformanceReport)
class PerformanceReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'employee', 'date_created', 'report_title')
    list_display_links = ('report_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'content')
    list_filter = ('date_created',)
    ordering = ('date_created',)

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'employee', 'review_date', 'reviewer', 'performance_score')
    list_display_links = ('review_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'review_comments', 'reviewer__first_name', 'reviewer__last_name')
    list_filter = ('review_date', 'performance_score')
    ordering = ('review_date',)

@admin.register(SanctionReport)
class SanctionReportAdmin(admin.ModelAdmin):
    list_display = ('sanction_id', 'employee', 'sanction_type', 'sanction_date', 'status')
    list_display_links = ('sanction_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'sanction_type')
    list_filter = ('status', 'sanction_date')
    ordering = ('sanction_date',)

@admin.register(Trainings)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('training_id', 'training_name', 'employee', 'start_date', 'end_date', 'status')
    search_fields = ('training_name', 'employee__first_name', 'employee__last_name', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    ordering = ('start_date',)
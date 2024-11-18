from django.contrib import admin
from django.contrib.auth.views import LoginView
from .models import Department, Job, EmployeeInformation, UserAccount, AttendanceRecord, EmployeePayroll, LeaveRequest, LeaveType, JobOpening, Applicant, PerformanceReport, PerformanceReview, SanctionReport, Trainings


class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'

class MyAdminSite(admin.AdminSite):
    site_header = 'HR Management System'
    login_template = 'admin/login.html'


admin.site.__class__ = MyAdminSite




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
    readonly_fields = ("profile_preview",)
    list_display = (
        'profile_preview', 'first_name', 'last_name', 'sex', 'address', 
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


@admin.register(EmployeePayroll)
class AdminPayrollAdmin(admin.ModelAdmin):
    list_display = (
        'payroll_id', 'employee', 'pay_period_start', 'pay_period_end', 
        'gross_salary', 'net_salary', 'hours_worked', 'overtime_hours'
    )
    list_display_links = ('payroll_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'payroll_id')
    list_filter = ('pay_period_start', 'pay_period_end')
    ordering = ('pay_period_start',)

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

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('job_opening_id', 'job', 'department', 'posting_date', 'application_deadline', 'closing_date')
    list_display_links = ('job_opening_id', 'job')
    search_fields = ('job__job_title', 'department__department_name', 'job_opening_id')
    list_filter = ('department', 'posting_date')
    ordering = ('posting_date',)

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = (
        'applicant_id', 'job_opening', 'first_name', 'last_name', 
        'email', 'phone','resume_preview', 'applicant_status'
    )
    readonly_fields = ('resume_preview',)
    list_display_links = ('applicant_id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'email', 'job_opening__job__job_title')
    list_filter = ('applicant_status', 'job_opening')
    ordering = ('first_name', 'last_name')

admin.site.site_header = 'HR Management System'

@admin.register(PerformanceReport)
class PerformanceReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'employee', 'date_created', 'report_title')  
    list_display_links = ('report_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'content')
    list_filter = ('date_created',)  
    ordering = ('date_created',)


@admin.register(SanctionReport)
class SanctionReportAdmin(admin.ModelAdmin):
    list_display = ('sanction_id', 'employee', 'sanction_type', 'sanction_date', 'status')
    list_display_links = ('sanction_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'sanction_type')
    list_filter = ('status', 'sanction_date')
    ordering = ('sanction_date',)



@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'employee', 'review_date', 'reviewer', 'performance_score')
    list_display_links = ('review_id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'review_comments', 'reviewer__first_name', 'reviewer__last_name')
    list_filter = ('review_date', 'performance_score')  
    ordering = ('review_date',)

@admin.register(Trainings)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('training_id', 'training_name', 'employee', 'start_date', 'end_date', 'status')
    search_fields = ('training_name', 'employee__first_name', 'employee__last_name', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    ordering = ('start_date',)
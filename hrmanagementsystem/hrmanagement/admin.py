from django.contrib import admin
from .models import AttendanceRecord, LeaveType, LeaveRequest, PerformanceReport, PerformanceReview, SanctionReport
from hraccount.models import EmployeeInformation

# Register your models here.
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
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
    list_filter = ('status', 'sanction_date', 'sanction_type')  # Add sanction_type to the filter
    ordering = ('sanction_date',)


from .models import PeerFeedback

@admin.register(PeerFeedback)
class PeerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'from_user', 'to_user', 'created_at')
    list_display_links = ('feedback_id', 'from_user')
    search_fields = ('from_user__first_name', 'from_user__last_name', 'to_user__first_name', 'to_user__last_name')
    list_filter = ('created_at',)
    ordering = ('created_at',)



from .models import SelfAssessment

@admin.register(SelfAssessment)
class SelfAssessmentAdmin(admin.ModelAdmin):
    list_display = ('self_assessment_id', 'employee', 'performance_rating', 'skill_development', 
                    'teamwork', 'communication_skills', 'company_culture', 
                    'work_life_balance', 'submitted_at')
    list_filter = ('performance_rating', 'teamwork', 'company_culture', 'submitted_at')
    search_fields = ('employee__first_name', 'employee__last_name', 'suggestions_for_improvement')
    ordering = ('-submitted_at',)


from django.contrib import admin
from .models import (
    JobPosting,
    JobApplication,
    Interview,
    OnboardingChecklist,
    OnboardingTask,
    EmployeeOnboarding,
    OnboardingTaskProgress
)

# Register your models here.

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'status', 'created_at')
    list_filter = ('status', 'department')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('get_applicant_name', 'email', 'job_posting', 'status', 'applied_at')
    list_filter = ('status', 'job_posting')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    date_hierarchy = 'applied_at'
    
    def get_applicant_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_applicant_name.short_description = 'Applicant Name'

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'interviewer', 'scheduled_at', 'status')
    list_filter = ('status',)
    search_fields = ('application__first_name', 'application__last_name', 'interviewer__first_name', 'interviewer__last_name')
    date_hierarchy = 'scheduled_at'

@admin.register(OnboardingChecklist)
class OnboardingChecklistAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(OnboardingTask)
class OnboardingTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'checklist', 'due_days')
    list_filter = ('checklist',)
    search_fields = ('title', 'description')
    ordering = ('checklist', 'title')

@admin.register(EmployeeOnboarding)
class EmployeeOnboardingAdmin(admin.ModelAdmin):
    list_display = ('employee', 'checklist', 'start_date', 'completed_at')
    list_filter = ('status',)
    search_fields = ('employee__first_name', 'employee__last_name')
    date_hierarchy = 'start_date'

@admin.register(OnboardingTaskProgress)
class OnboardingTaskProgressAdmin(admin.ModelAdmin):
    list_display = ('employee_onboarding', 'task', 'status', 'completed_at')
    list_filter = ('status',)
    search_fields = ('employee_onboarding__employee__first_name', 'employee_onboarding__employee__last_name', 'task__title')
    date_hierarchy = 'completed_at'

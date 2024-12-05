from django.contrib import admin
from .models import (
    JobPosting,
    JobApplication,
    Interview,
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

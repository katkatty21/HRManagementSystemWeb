from django.db import models
from hrmanagement.models import EmployeeInformation
from hraccount.models import Job, Department
import uuid

class JobPosting(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('CONTRACT', 'Contract'),
        ('INTERNSHIP', 'Internship'),
    ]
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_postings', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='job_postings')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    qualifications = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closing_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.department}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('REVIEWING', 'Reviewing'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEW_SCHEDULED', 'Interview Scheduled'),
        ('INTERVIEWED', 'Interviewed'),
        ('OFFERED', 'Offered'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
    ]
    
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_posting.title}"

class Interview(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('RESCHEDULED', 'Rescheduled'),
    ]
    
    RECOMMENDATION_CHOICES = [
        ('hire', 'Recommend to Hire'),
        ('reject', 'Do Not Recommend'),
        ('consider', 'Consider for Other Positions'),
    ]
    
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(EmployeeInformation, on_delete=models.SET_NULL, null=True)
    scheduled_at = models.DateTimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=200)  # Can be physical location or virtual meeting link
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    feedback = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True, help_text='Interview rating from 1-5')
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATION_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return f"Interview for {self.application} with {self.interviewer}"

class OnboardingChecklist(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class OnboardingTask(models.Model):
    checklist = models.ForeignKey(OnboardingChecklist, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_days = models.IntegerField(help_text='Days from start date to complete this task')
    assigned_to_hr = models.BooleanField(default=False)
    required_documents = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.checklist.title}"

class EmployeeOnboarding(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
    ]
    
    employee = models.OneToOneField(EmployeeInformation, on_delete=models.CASCADE)
    checklist = models.ForeignKey(OnboardingChecklist, on_delete=models.CASCADE)
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Onboarding for {self.employee}"
    
    def calculate_progress(self):
        total_tasks = self.task_progress.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.task_progress.filter(status='COMPLETED').count()
        return (completed_tasks / total_tasks) * 100

class OnboardingTaskProgress(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('BLOCKED', 'Blocked'),
    ]
    
    employee_onboarding = models.ForeignKey(EmployeeOnboarding, on_delete=models.CASCADE, related_name='task_progress')
    task = models.ForeignKey(OnboardingTask, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    documents = models.FileField(upload_to='onboarding_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['employee_onboarding', 'task']
        verbose_name_plural = 'Onboarding task progress'
    
    def __str__(self):
        return f"{self.task.title} - {self.employee_onboarding.employee}"

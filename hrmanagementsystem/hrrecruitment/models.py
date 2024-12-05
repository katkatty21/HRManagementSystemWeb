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


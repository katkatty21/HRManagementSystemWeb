import uuid
import os
from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import AbstractUser
from enum import Enum

class JobStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    FILLED = 'filled'

# UserAccount Model
class UserAccount(AbstractUser):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=20, 
        choices=[('Admin', 'Admin'), ('User', 'User')], 
        default='User', 
        blank=False
    )
    date_account_added = models.DateField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'role']  # Add 'role' to required fields

    def save(self, *args, **kwargs):
        # Always use email from EmployeeInformation as username
        self.username = self.email  # Use email as username

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


# Department Model
class Department(models.Model):
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.CharField(max_length=500)

    def __str__(self):
        return self.department_name

# Job Model
class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50)
    salary_range = models.CharField(max_length=50, blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[(status.name, status.value) for status in JobStatus], default=JobStatus.OPEN)

    def __str__(self):
        return self.job_title

# EmployeeInformation Model
class EmployeeInformation(models.Model):

    def upload_profile_picture(instance, filename):
        ext = filename.split('.')[-1]  # Get file extension
        filename = f"{instance.first_name}_{instance.last_name}_{uuid.uuid4()}.{ext}"  # Generate unique filename
        return os.path.join('photos', 'employees', filename)

    SEX_CHOICES = [
        ('Choose', 'Choose'),
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
    ]

    employee_id = models.OneToOneField(
        'UserAccount',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='employee_information'
    )
    profile_picture = models.ImageField(upload_to=upload_profile_picture, null=True, blank=True)  # Updated field
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, default='Choose')
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='Single')
    nationality = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    active_phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    date_hired = models.DateField()
    employment_status = models.CharField(max_length=20)
    sss_number = models.CharField(max_length=20)
    pagibig_number = models.CharField(max_length=20)
    philhealth_number = models.CharField(max_length=20)
    tin_number = models.CharField(max_length=20)
    bank_account_number = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=50)
    emergency_contact_rs = models.CharField(max_length=50)
    emergency_contact_number = models.CharField(max_length=20)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="employee_jobs")

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        if self.employee_id:
            self.email = self.employee_id.email  # Ensure email is synced from UserAccount
        super().save(*args, **kwargs)

    def profile_preview(self):
        """
        Display profile picture as an HTML image tag.
        """
        if self.profile_picture:
            # If profile picture exists, return the HTML image tag
            return mark_safe(f'<img src="{self.profile_picture.url}" width="50" height="50" />')
        return "No Profile Picture"  # If no profile picture, return a placeholder text
     
import uuid
import base64
from django.db import models
from django.utils.html import mark_safe
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import AbstractUser

# UserAccount Model
class UserAccount(AbstractUser):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=20, 
        choices=[('Admin', 'Admin'), ('User', 'User')], 
        default='User', 
        blank=False  # Ensures role is not blank
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
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="jobs")
    job_title = models.CharField(max_length=50)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.job_title

# EmployeeInformation Model
class EmployeeInformation(models.Model):
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
    profile_picture = models.BinaryField(null=True, blank=True)
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
    role = models.CharField(
        max_length=20,
        choices=[('Admin', 'Admin'), ('User', 'User')],
        default='User'
    )
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="employee_jobs")

    def save(self, *args, **kwargs):
        if self.employee_id:
            self.email = self.employee_id.email  # Ensure email is synced from UserAccount
        super().save(*args, **kwargs)

    def save_profile_picture(self, image_file):
        """
        Save profile picture as binary data.
        """
        img = Image.open(image_file)
        img_format = img.format.lower()

        if img_format not in ['png', 'jpeg', 'jpg']:
            raise ValueError("Only PNG or JPEG files are supported")

        img_io = BytesIO()
        img.save(img_io, format=img_format.upper())
        img_io.seek(0)
        self.profile_picture = img_io.read()

    def profile_preview(self):
        """
        Display profile picture in admin panel or frontend as an HTML image.
        """
        if self.profile_picture:
            img_data = base64.b64encode(self.profile_picture).decode('utf-8')
            return mark_safe(f'<img src="data:image/png;base64,{img_data}" width="50" height="50" style="border-radius: 50%;" />')
        return None

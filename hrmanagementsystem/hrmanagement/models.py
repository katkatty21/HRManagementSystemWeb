import uuid
import string
import os
import random
from django.db import models
from django.utils.html import mark_safe, format_html
from datetime import datetime

class Department(models.Model):
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.CharField(max_length=500)

    def __str__(self):
        return self.department_name


class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="jobs")
    job_title = models.CharField(max_length=50)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.job_title

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

    def upload_profile_picture(instance, filename):
        ext = filename.split('.')[-1]  # Get file extension
        # Generate filename with first name, last name, and UUID to ensure uniqueness
        filename = f"{instance.first_name}_{instance.last_name}_{uuid.uuid4()}.{ext}"
        return os.path.join('photos', 'employees', filename)

    employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField(upload_to=upload_profile_picture)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    sex = models.CharField(
        max_length=20,
        choices=SEX_CHOICES,
        default='Choose'
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        default='Single'
    )
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
        choices=[
            ('Admin', 'Admin'),
            ('User', 'User'),
        ],
        default='User'
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="employee_jobs")

    def profile_preview(self):
        return mark_safe(f'<img src="{self.profile_picture.url}" alt="" width="50px" height="50px" style="border-radius: 50%;"/>')


    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"



class UserAccount(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]

    account_id = models.OneToOneField(EmployeeInformation, on_delete=models.CASCADE, primary_key=True, related_name='user_account')
    username = models.EmailField(max_length=100, unique=True)  # Changed to EmailField
    password = models.CharField(max_length=50)
    date_account_added = models.DateField(auto_now=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='User'
    )

    def generate_password(self):
        """
        Generates a password in the format: lastname.[A-Z][a-z][0-9][0-9][0-9]
        Example: doe.Xy123
        """
        lastname = self.account_id.last_name.lower()
        upper_letter = random.choice(string.ascii_uppercase)
        lower_letter = random.choice(string.ascii_lowercase)
        numbers = ''.join(random.choices(string.digits, k=3))
        
        return f"{lastname}.{upper_letter}{lower_letter}{numbers}"

    def save(self, *args, **kwargs):
        # Always use email from EmployeeInformation as username
        self.username = self.account_id.email
        
        if not self.password:
            self.password = self.generate_password()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

##Sophie Seismundo

class EmployeePayroll(models.Model):
    payroll_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE, related_name='payrolls')
    pay_period_start = models.DateField()
    pay_period_end = models.DateField() #default 30 days after start 
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sss_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pagibig_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    philhealth_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payroll {self.payroll_id} for {self.employee}"
    

class AttendanceRecord(models.Model):
    attendance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')], default='Absent')

    def calculate_total_hours(self):
        if self.time_in and self.time_out:
            time_in_datetime = datetime.combine(self.date, self.time_in)
            time_out_datetime = datetime.combine(self.date, self.time_out)
            elapsed_time = time_out_datetime - time_in_datetime
            total_seconds = elapsed_time.total_seconds()
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return round(hours + minutes / 60, 2)  # Convert to decimal format
        return 0.00

    def __str__(self):
        return f"Attendance {self.attendance_id} for {self.employee} on {self.date}"


class LeaveType(models.Model):
    leave_type_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leave_name = models.CharField(max_length=50)
    max_days_allowed = models.IntegerField()

    def __str__(self):
        return f"{self.leave_name} {self.max_days_allowed}"
    
class LeaveRequest(models.Model):
    leave_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_requests')
    description = models.CharField(max_length=500, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"Leave {self.leave_id} for {self.employee}"

class JobOpening(models.Model):
    job_opening_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="openings")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="openings")
    posting_date = models.DateField()
    application_deadline = models.DateField()
    closing_date = models.DateField(null=True, blank=True)  
    def __str__(self):
        return f"Opening for {self.job.job_title} in {self.department.department_name}"

def generate_custom_applicant_id():
    random_digits = f"{random.randint(10000, 99999)}"
    random_letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=4))
    random_suffix = f"{random.randint(100, 999)}"
    return f"Applicant-{random_digits}-{random_letters}-{random_suffix}"

def upload_resume(instance, filename):
    # Extract the file extension
    ext = filename.split('.')[-1]
    # Create a new filename with the applicant's first and last name
    filename = f"{instance.first_name}_{instance.last_name}_resume.{ext}"
    return os.path.join('uploads/resumes/', filename)

class Applicant(models.Model):
    applicant_id = models.CharField(
        max_length=30, 
        primary_key=True, 
        editable=False, 
        default=generate_custom_applicant_id
    )
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name="applicants")
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    resume = models.FileField(upload_to=upload_resume)  
    interview_date = models.DateField(null=True, blank=True)
    applicant_status = models.CharField(max_length=20, choices=[
        ('Applied', 'Applied'), 
        ('Interviewed', 'Interviewed'), 
        ('Hired', 'Hired'), 
        ('Rejected', 'Rejected')
    ], default='Applied')

    def resume_preview(self):
        if self.resume:
            return format_html(f'<a href="{self.resume.url}" target="_blank">View Resume</a>')
        return "No resume uploaded"

    resume_preview.short_description = "Resume Preview"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_opening.job.job_title}"

class PerformanceReport(models.Model):
    report_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE, related_name='performance_reports')
    report_title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateField(auto_now_add=True)  # This is used as the "submission date"

    def __str__(self):
        return f"{self.report_title} - {self.employee.first_name} {self.employee.last_name}"



class SanctionReport(models.Model):
    sanction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE, related_name='sanction_reports')
    sanction_reason = models.CharField(max_length=255)
    sanction_details = models.TextField()
    sanction_type = models.CharField(max_length=255)  
    sanction_date = models.DateField()  
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Resolved', 'Resolved')])  
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sanction for {self.employee.first_name} {self.employee.last_name}: {self.sanction_reason}"



class PerformanceReview(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE, related_name='performance_reviews')
    reviewer = models.ForeignKey(EmployeeInformation, on_delete=models.SET_NULL, null=True, related_name='reviews_given')
    review_comments = models.TextField()
    review_date = models.DateField(auto_now_add=True)
    overall_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    performance_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) 

    def __str__(self):
        return f"Review by {self.reviewer.first_name} {self.reviewer.last_name} for {self.employee.first_name} {self.employee.last_name}"
    
class Trainings(models.Model):
    training_id = models.CharField(max_length=10, primary_key=True)
    employee = models.ForeignKey(
        EmployeeInformation, on_delete=models.CASCADE, related_name="trainings", db_column="employee_id"
    )
    training_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Scheduled', 'Scheduled'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], default='Scheduled')

    def __str__(self):
        return f"{self.training_name} ({self.employee.first_name} {self.employee.last_name})"

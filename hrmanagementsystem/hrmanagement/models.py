import uuid
from django.db import models

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

    employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField(upload_to='photos/%Y/%m/%d/')
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

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"



class UserAccount(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]

    account_id = models.OneToOneField(EmployeeInformation, on_delete=models.CASCADE, primary_key=True, related_name='user_account')
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=20)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='User'
    )

    def __str__(self):
        return self.username

##Sophie Seismundo

class AdminPayroll(models.Model):
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
    date = models.DateField()
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')], default='Absent')

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

class Applicant(models.Model):
    applicant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name="applicants")
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    resume = models.FileField(upload_to='uploads/resumes/')  
    interview_date = models.DateField(null=True, blank=True)
    applicant_status = models.CharField(max_length=20, choices=[
        ('Applied', 'Applied'), 
        ('Interviewed', 'Interviewed'), 
        ('Hired', 'Hired'), 
        ('Rejected', 'Rejected')
    ], default='Applied')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_opening.job.job_title}"
    
class Training(models.Model):
    training_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE, related_name='trainings')
    training_name = models.CharField(max_length=500)
    description = models.TextField
    
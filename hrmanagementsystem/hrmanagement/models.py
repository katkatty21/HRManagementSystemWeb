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

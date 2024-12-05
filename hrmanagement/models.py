from django.db import models
from django.conf import settings
from hraccount.models import EmployeeInformation
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class PayrollPeriod(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    PERIOD_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('SEMI-MONTHLY', 'Semi-Monthly'),
        ('WEEKLY', 'Weekly'),
    ]
    
    start_date = models.DateField()
    end_date = models.DateField()
    period_type = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.period_type} Period: {self.start_date} to {self.end_date}"

class EmployeeSalary(models.Model):
    PAY_TYPE_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('HOURLY', 'Hourly'),
    ]
    
    employee = models.OneToOneField(EmployeeInformation, on_delete=models.CASCADE)
    pay_type = models.CharField(max_length=10, choices=PAY_TYPE_CHOICES)
    base_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    effective_date = models.DateField()
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.pay_type} - {self.base_salary}"

class PayrollAdjustment(models.Model):
    ADJUSTMENT_TYPE_CHOICES = [
        ('BONUS', 'Bonus'),
        ('DEDUCTION', 'Deduction'),
    ]
    
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.adjustment_type} - {self.amount}"

class PayrollRecord(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_finalized = models.BooleanField(default=False)
    date_processed = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['employee', 'payroll_period']
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.payroll_period}"

class PayrollCorrectionRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    employee = models.ForeignKey(EmployeeInformation, on_delete=models.CASCADE)
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    date_submitted = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_corrections')
    admin_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Correction Request - {self.employee} - {self.date_submitted.strftime('%Y-%m-%d')}"

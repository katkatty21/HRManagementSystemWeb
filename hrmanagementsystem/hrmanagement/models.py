from django.db import models
from hraccount.models import EmployeeInformation
import uuid
import string
import os
import random
from django.db import models
from django.utils.html import mark_safe, format_html
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
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
            time_in = datetime.combine(self.date, self.time_in)
            time_out = datetime.combine(self.date, self.time_out)
            elapsed_time = time_out - time_in  # timedelta object
            elapsed_minutes = elapsed_time.total_seconds() / 60  # Convert to minutes
            return round(elapsed_minutes / 60, 2)  # Convert to hours (decimal)
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
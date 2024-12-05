# Generated by Django 5.1.2 on 2024-11-03 16:23

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanagement', '0002_remove_employeeinformation_gender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveType',
            fields=[
                ('leave_type_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('leave_name', models.CharField(max_length=50)),
                ('max_days_allowed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AdminPayroll',
            fields=[
                ('payroll_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pay_period_start', models.DateField()),
                ('pay_period_end', models.DateField()),
                ('hours_worked', models.DecimalField(decimal_places=2, max_digits=5)),
                ('overtime_hours', models.DecimalField(decimal_places=2, max_digits=5)),
                ('gross_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax_deduction', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sss_deduction', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('pagibig_deduction', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('philhealth_deduction', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payrolls', to='hrmanagement.employeeinformation')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('attendance_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time_in', models.TimeField(blank=True, null=True)),
                ('time_out', models.TimeField(blank=True, null=True)),
                ('total_hours', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')], default='Absent', max_length=20)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='hrmanagement.employeeinformation')),
            ],
        ),
        migrations.CreateModel(
            name='JobOpening',
            fields=[
                ('job_opening_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('posting_date', models.DateField()),
                ('application_deadline', models.DateField()),
                ('closing_date', models.DateField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='openings', to='hrmanagement.department')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='openings', to='hrmanagement.job')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('applicant_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('resume', models.FileField(upload_to='uploads/resumes/')),
                ('interview_date', models.DateField(blank=True, null=True)),
                ('applicant_status', models.CharField(choices=[('Applied', 'Applied'), ('Interviewed', 'Interviewed'), ('Hired', 'Hired'), ('Rejected', 'Rejected')], default='Applied', max_length=20)),
                ('job_opening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='hrmanagement.jobopening')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('leave_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('duration', models.IntegerField()),
                ('reason', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to='hrmanagement.employeeinformation')),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to='hrmanagement.leavetype')),
            ],
        ),
    ]
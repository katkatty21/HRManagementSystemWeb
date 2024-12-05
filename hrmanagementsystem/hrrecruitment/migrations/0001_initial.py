# Generated by Django 5.1.3 on 2024-12-05 04:15

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hraccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('resume', models.FileField(upload_to='resumes/')),
                ('cover_letter', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('REVIEWING', 'Reviewing'), ('SHORTLISTED', 'Shortlisted'), ('INTERVIEW_SCHEDULED', 'Interview Scheduled'), ('INTERVIEWED', 'Interviewed'), ('OFFERED', 'Offered'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('WITHDRAWN', 'Withdrawn')], default='NEW', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_at', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('location', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('SCHEDULED', 'Scheduled'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('RESCHEDULED', 'Rescheduled')], default='SCHEDULED', max_length=20)),
                ('feedback', models.TextField(blank=True)),
                ('rating', models.IntegerField(blank=True, help_text='Interview rating from 1-5', null=True)),
                ('recommendation', models.CharField(blank=True, choices=[('hire', 'Recommend to Hire'), ('reject', 'Do Not Recommend'), ('consider', 'Consider for Other Positions')], max_length=20, null=True)),
                ('interviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hraccount.employeeinformation')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='hrrecruitment.jobapplication')),
            ],
        ),
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('employment_type', models.CharField(choices=[('FULL_TIME', 'Full Time'), ('PART_TIME', 'Part Time'), ('CONTRACT', 'Contract'), ('INTERNSHIP', 'Internship')], max_length=20)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('qualifications', models.TextField(blank=True)),
                ('benefits', models.TextField(blank=True)),
                ('salary_range', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('OPEN', 'Open'), ('CLOSED', 'Closed')], default='DRAFT', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('closing_date', models.DateField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_postings', to='hraccount.department')),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_postings', to='hraccount.job')),
            ],
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='job_posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='hrrecruitment.jobposting'),
        ),
    ]

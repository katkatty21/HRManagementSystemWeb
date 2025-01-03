# Generated by Django 5.1.3 on 2024-12-03 16:07

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import hraccount.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('account_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('User', 'User')], default='User', max_length=20)),
                ('date_account_added', models.DateField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('job_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=50)),
                ('salary_range', models.CharField(blank=True, max_length=50, null=True)),
                ('job_description', models.TextField(blank=True, null=True)),
                ('requirements', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('OPEN', 'open'), ('CLOSED', 'closed'), ('FILLED', 'filled')], default=hraccount.models.JobStatus['OPEN'], max_length=20)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hraccount.department')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeInformation',
            fields=[
                ('employee_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='employee_information', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=hraccount.models.EmployeeInformation.upload_profile_picture)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('sex', models.CharField(choices=[('Choose', 'Choose'), ('Female', 'Female'), ('Male', 'Male')], default='Choose', max_length=20)),
                ('marital_status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Widowed', 'Widowed')], default='Single', max_length=20)),
                ('nationality', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=20)),
                ('active_phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('date_hired', models.DateField()),
                ('employment_status', models.CharField(max_length=20)),
                ('sss_number', models.CharField(max_length=20)),
                ('pagibig_number', models.CharField(max_length=20)),
                ('philhealth_number', models.CharField(max_length=20)),
                ('tin_number', models.CharField(max_length=20)),
                ('bank_account_number', models.CharField(max_length=20)),
                ('emergency_contact_name', models.CharField(max_length=50)),
                ('emergency_contact_rs', models.CharField(max_length=50)),
                ('emergency_contact_number', models.CharField(max_length=20)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_jobs', to='hraccount.job')),
            ],
        ),
    ]

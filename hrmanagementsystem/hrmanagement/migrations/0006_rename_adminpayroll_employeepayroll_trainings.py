# Generated by Django 5.1.2 on 2024-11-18 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanagement', '0005_alter_applicant_resume_performancereport_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdminPayroll',
            new_name='EmployeePayroll',
        ),
        migrations.CreateModel(
            name='Trainings',
            fields=[
                ('training_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('training_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled', max_length=20)),
                ('employee', models.ForeignKey(db_column='employee_id', on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to='hrmanagement.employeeinformation')),
            ],
        ),
    ]
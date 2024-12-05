# Generated by Django 5.1.2 on 2024-11-02 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanagement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeinformation',
            name='gender',
        ),
        migrations.AddField(
            model_name='employeeinformation',
            name='sex',
            field=models.CharField(choices=[('Choose', 'Choose'), ('Female', 'Female'), ('Male', 'Male')], default='Choose', max_length=20),
        ),
        migrations.AlterField(
            model_name='employeeinformation',
            name='active_phone_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='employeeinformation',
            name='emergency_contact_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='employeeinformation',
            name='employment_status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='employeeinformation',
            name='marital_status',
            field=models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Widowed', 'Widowed')], default='Single', max_length=20),
        ),
        migrations.AlterField(
            model_name='employeeinformation',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('User', 'User')], default='User', max_length=20),
        ),
        migrations.AlterField(
            model_name='employeeinformation',
            name='zip_code',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='password',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('User', 'User')], default='User', max_length=20),
        ),
    ]
# Generated by Django 5.1.3 on 2024-11-07 11:58

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanagement', '0004_training'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceReport',
            fields=[
                ('report_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('report_title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_reports', to='hrmanagement.employeeinformation')),
            ],
        ),
    ]
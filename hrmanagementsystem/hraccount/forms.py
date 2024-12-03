from django import forms
from .models import Department, Job, EmployeeInformation
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_title', 'department', 'status', 'job_description', 'salary_range', 'requirements']  # Use the actual model fields
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'salary': forms.NumberInput(attrs={'step': 1000}),
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        # Optional: you can set initial values if needed
        self.fields['department'].empty_label = "Select Department"  # Avoid "None" appearing
        self.fields['status'].empty_label = "Select Status"  # 
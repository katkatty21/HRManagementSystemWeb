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


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeInformation
        fields = [
            'first_name','middle_name', 'last_name', 'email', 'profile_picture', 'job', 
            'sex', 'marital_status', 'nationality', 'address', 'city', 'province',
            'zip_code', 'active_phone_number', 'date_hired', 'employment_status', 
            'sss_number', 'pagibig_number', 'philhealth_number', 'tin_number', 
            'bank_account_number', 'emergency_contact_name', 'emergency_contact_rs', 
            'emergency_contact_number'
        ]
        widgets = {
            'profile_picture': forms.ClearableFileInput(),  # Remove 'multiple' here
            'date_hired': forms.DateInput(attrs={'type': 'date'}),
        }
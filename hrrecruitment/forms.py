from django import forms
from .models import (
    JobPosting,
    JobApplication,
    Interview,
    OnboardingChecklist,
    OnboardingTask,
    OnboardingTaskProgress
)
from hraccount.models import Job, Department
from datetime import datetime

class JobPostingForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select a department...",
        to_field_name='department_id'
    )
    job = forms.ModelChoiceField(
        queryset=Job.objects.all(),
        empty_label="Select a job...",
        required=False,
        to_field_name='job_id'
    )
    status = forms.ChoiceField(
        choices=JobPosting.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='DRAFT'
    )

    class Meta:
        model = JobPosting
        fields = [
            'title', 'department', 'job', 'employment_type', 'location',
            'description', 'requirements', 'qualifications', 'benefits',
            'salary_range', 'status', 'closing_date'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'qualifications': forms.Textarea(attrs={'rows': 4}),
            'benefits': forms.Textarea(attrs={'rows': 4}),
            'employment_type': forms.Select(choices=JobPosting.EMPLOYMENT_TYPE_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure closing date widget
        self.fields['closing_date'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': datetime.now().strftime('%Y-%m-%d')  # Prevent past dates
        })
        
        # Update job choices based on department if department is selected
        if 'department' in self.data:
            try:
                department_id = self.data.get('department')
                self.fields['job'].queryset = Job.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.department:
            self.fields['job'].queryset = Job.objects.filter(department=self.instance.department)
        
        # Add form-control class to all fields for consistent styling
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
        
        if self.instance.pk:
            # For editing existing job posting
            if self.instance.department:
                self.fields['department'].initial = self.instance.department.department_id  # Use UUID
                self.fields['job'].initial = self.instance.job.job_id  # Use UUID
            if self.instance.closing_date:
                # Set both initial and widget value for the closing date
                self.fields['closing_date'].initial = self.instance.closing_date
                self.fields['closing_date'].widget.attrs['value'] = self.instance.closing_date.strftime('%Y-%m-%d')
            if self.instance.status:
                self.fields['status'].initial = self.instance.status

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        job = cleaned_data.get('job')
        closing_date = cleaned_data.get('closing_date')

        if job and department and job.department_id != department.department_id:
            raise forms.ValidationError('Selected job does not belong to the selected department.')

        if closing_date and closing_date < datetime.now().date():
            raise forms.ValidationError('Closing date cannot be in the past.')

        return cleaned_data

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'resume', 'cover_letter'
        ]
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
            'resume': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'})
        }
        
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Get file extension
            file_ext = resume.name.split('.')[-1].lower()
            # Check if file extension is allowed
            if file_ext not in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError(
                    'Only PDF and Word documents are allowed.'
                )
            # Check file size (max 5MB)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'File size must not exceed 5MB.'
                )
        return resume

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3})
        }

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interviewer', 'scheduled_at', 'duration', 'location']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'})
        }

class InterviewFeedbackForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['feedback', 'rating', 'recommendation']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
            'recommendation': forms.Select(choices=[
                ('hire', 'Recommend to Hire'),
                ('reject', 'Do Not Recommend'),
                ('consider', 'Consider for Other Positions')
            ])
        }

class OnboardingChecklistForm(forms.ModelForm):
    class Meta:
        model = OnboardingChecklist
        fields = ['title', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }

class OnboardingTaskForm(forms.ModelForm):
    class Meta:
        model = OnboardingTask
        fields = [
            'title', 'description', 'due_days',
            'assigned_to_hr', 'required_documents'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'required_documents': forms.Textarea(attrs={'rows': 2})
        }

class TaskProgressForm(forms.ModelForm):
    class Meta:
        model = OnboardingTaskProgress
        fields = ['status', 'notes', 'documents']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3})
        }

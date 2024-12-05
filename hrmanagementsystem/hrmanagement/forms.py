from django import forms
from .models import LeaveRequest
from .models import (
    PayrollPeriod,
    PayrollAdjustment,
    PayrollCorrectionRequest,
)

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'description', 'reason']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PayrollPeriodForm(forms.ModelForm):
    class Meta:
        model = PayrollPeriod
        fields = ['start_date', 'end_date', 'period_type']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PayrollAdjustmentForm(forms.ModelForm):
    class Meta:
        model = PayrollAdjustment
        fields = ['employee', 'adjustment_type', 'amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PayrollCorrectionRequestForm(forms.ModelForm):
    class Meta:
        model = PayrollCorrectionRequest
        fields = ['payroll_record', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
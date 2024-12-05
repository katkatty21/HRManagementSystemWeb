from django.contrib import admin
from .models import (
    PayrollPeriod,
    EmployeeSalary,
    PayrollRecord,
    PayrollCorrectionRequest,
    PayrollAdjustment
)

# Register your models here.

@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'period_type', 'is_processed')
    list_filter = ('period_type', 'is_processed')
    search_fields = ('start_date', 'end_date')
    ordering = ('-start_date',)

@admin.register(EmployeeSalary)
class EmployeeSalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'pay_type', 'base_salary', 'effective_date')
    list_filter = ('pay_type',)
    search_fields = ('employee__first_name', 'employee__last_name')
    ordering = ('employee__last_name',)

@admin.register(PayrollRecord)
class PayrollRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payroll_period', 'base_salary', 'total_bonus', 
                   'total_deduction', 'net_salary', 'is_finalized')
    list_filter = ('payroll_period', 'is_finalized')
    search_fields = ('employee__first_name', 'employee__last_name')
    ordering = ('-date_processed',)
    readonly_fields = ('date_processed',)

@admin.register(PayrollAdjustment)
class PayrollAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payroll_period', 'adjustment_type', 'amount', 'description', 'date_added')
    list_filter = ('adjustment_type', 'payroll_period')
    search_fields = ('employee__first_name', 'employee__last_name', 'description')

@admin.register(PayrollCorrectionRequest)
class PayrollCorrectionRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payroll_record', 'status', 'date_submitted', 'processed_at')
    list_filter = ('status',)
    search_fields = ('employee__first_name', 'employee__last_name', 'description')
    ordering = ('-date_submitted',)
    readonly_fields = ('date_submitted',)

from django.urls import path
from . import views

app_name = 'hrmanagement'

urlpatterns = [
    # Admin URLs
    path('admin/payroll/periods/', views.manage_payroll_period, name='payroll_periods'),
    path('admin/payroll/salaries/', views.manage_employee_salary, name='employee_salaries'),
    path('admin/payroll/adjustments/', views.manage_payroll_adjustment, name='payroll_adjustments'),
    path('admin/payroll/process/<uuid:period_id>/', views.process_payroll, name='process_payroll'),
    path('admin/payroll/export/<uuid:period_id>/', views.export_payroll, name='export_payroll'),
    path('admin/payroll/corrections/', views.manage_correction_requests, name='correction_requests'),
    
    # Employee URLs
    path('payroll/', views.view_payroll, name='view_payroll'),
    path('payroll/<int:record_id>/', views.view_payroll_detail, name='payroll_detail'),
    path('payroll/<int:record_id>/download/', views.download_payslip, name='download_payslip'),
    path('payroll/correction/submit/', views.submit_correction_request, name='submit_correction'),
    
    # Correction Request Actions
    path('admin/correction/approve/<int:request_id>/', views.approve_correction_request, name='approve_correction'),
    path('admin/correction/reject/<int:request_id>/', views.reject_correction_request, name='reject_correction'),
]

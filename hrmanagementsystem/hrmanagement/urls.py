from django.urls import path
from . import views

urlpatterns = [
    path('hr/admin/employee/clock-in/', views.admin_clock_in, name='admin_clock_in'),
    path('hr/admin/employee/clock-out/', views.admin_clock_out, name='admin_clock_out'),
    path('hr/admin/attendance/', views.admin_attendance_list, name='admin_attendance_list'),
    path('hr/admin/leave/', views.leave_list, name='leave_list'),
    path('hr/admin/performance-management/', views.performance_management, name='performance_management'),
    path('hr/admin/sanction/<uuid:sanction_id>/update-status/', views.update_status, name='update_status'),
    path('hr/admin/payroll/periods/', views.manage_payroll_period, name='payroll_periods'),
    path('hr/admin/payroll/salaries/', views.manage_employee_salary, name='employee_salaries'),
    path('hr/admin/payroll/process/<uuid:period_id>/', views.process_payroll, name='process_payroll'),
    path('hr/admin/payroll/export/<uuid:period_id>/', views.export_payroll, name='export_payroll'),

    path('hr/employee/clock-in/', views.user_clock_in, name='user_clock_in'),
    path('hr/employee/clock-out/', views.user_clock_out, name='user_clock_out'),
    path('hr/employee/leave_request/', views.leave_request, name='leave_request'),
    path('hr/employee/attendance-record/', views.attendance_record, name='attendance_record'),
    path('hr/employee/performance_feedback/', views.performance_feedback, name='performance_feedback'), 
    path('hr/employee/peer_feedback/', views.peer_feedback, name='peer_feedback'),
    path('hr/employee/self-assessment/', views.self_assessment_view, name='self_assessment'),
    path('hr/employee/payroll/', views.view_payroll, name='view_payroll'),
    path('hr/employee/payroll/<int:record_id>/', views.view_payroll_detail, name='payroll_detail'),
    path('hr/employee/payroll/<int:record_id>/download/', views.download_payslip, name='download_payslip'),
    path('hr/employee/payroll/correction/submit/', views.submit_correction_request, name='submit_correction'),

    
]

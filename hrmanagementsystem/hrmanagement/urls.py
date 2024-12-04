from django.urls import path
from . import views

urlpatterns = [
    path('hr/admin/employee/clock-in/', views.admin_clock_in, name='admin_clock_in'),
    path('hr/admin/employee/clock-out/', views.admin_clock_out, name='admin_clock_out'),

    path('hr/admin/attendance/', views.attendance_list, name='attendance_list'),

    path('hr/employee/clock-in/', views.user_clock_in, name='user_clock_in'),
    path('hr/employee/clock-out/', views.user_clock_out, name='user_clock_out'),

    path('hr/admin/leave/', views.leave_list, name='leave_list'),
    path('hr/admin/performance-management/', views.performance_management, name='performance_management'),
    path('hr/admin/sanction/<uuid:sanction_id>/update-status/', views.update_status, name='update_status'),


     ##user


    path('leave_request/', views.leave_request, name='leave_request'),
    path('attendance-record/', views.attendance_record, name='attendance_record'),
    path('performance_feedback/', views.performance_feedback, name='performance_feedback'), 
    path('peer_feedback/', views.peer_feedback, name='peer_feedback'),
    path('self-assessment/', views.self_assessment_view, name='self_assessment')

  
    
    
]

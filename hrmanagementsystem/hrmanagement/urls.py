from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'), 
    path('home/', views.home, name='home'), 
    path('clock-in/', views.clock_in, name='clock_in'),
    path('attendance-record/', views.attendance_record, name='attendance_record'), 
    path('admin/login/', views.custom_admin_login, name='admin_login'),
    path('leave_request/', views.leave_request_page, name='leave_request_page'),
    path('performance_feedback/', views.performance_feedback, name='performance_feedback'),
    path('peer_feedback/', views.peer_feedback, name='peer_feedback'),
    path('self-assessment/', views.self_assessment_view, name='self_assessment')

]

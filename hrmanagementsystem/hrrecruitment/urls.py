from django.urls import path
from . import views

urlpatterns = [
    # API Endpoints
    path('hr/admin/api/departments/<str:department_id>/jobs/', views.get_department_jobs, name='get_department_jobs'),
    
    path('', views.public_job_listings, name='careers_home'),
    path('jobs/<str:job_id>/', views.job_detail, name='job_detail'),
    path('application/<str:application_id>/success/', views.application_success, name='application_success'),
    
    path('hr/employee/job-postings/', views.job_postings_list, name='job_postings'),
    
    path('hr/admin/jobs/', views.admin_job_postings, name='admin_job_postings'),
    path('hr/admin/jobs/create/', views.create_job_posting, name='create_job_posting'),
    path('hr/admin/jobs/<str:posting_id>/edit/', views.edit_job_posting, name='edit_job_posting'),
    path('hr/admin/jobs/<str:posting_id>/delete/', views.delete_job_posting, name='delete_job_posting'),
    
    path('hr/admin/applications/', views.job_applications, name='job_applications'),
    path('hr/admin/applications/<str:application_id>/', views.application_detail, name='application_detail'),
    path('hr/admin/applications/<str:application_id>/status/', views.update_application_status, name='update_application_status'),
    
    path('hr/admin/applications/', views.applications_list, name='applications_list'),
    path('hr/admin/api/applications/<str:application_id>/', views.application_detail, name='application_detail'),
    path('hr/admin/api/applications/<str:application_id>/status/', views.update_application_status, name='update_application_status'),
    path('hr/admin/applications/<str:application_id>/resume/', views.download_resume, name='download_resume'),
    
    path('hr/admin/interviews/', views.interviews, name='interviews'),
    path('hr/admin/applications/<str:application_id>/schedule-interview/', views.schedule_interview, name='schedule_interview'),
    path('hr/admin/interviews/<str:interview_id>/edit/', views.edit_interview, name='edit_interview'),
    path('hr/admin/interviews/<str:interview_id>/cancel/', views.cancel_interview, name='cancel_interview'),
    path('hr/admin/interviews/<str:interview_id>/feedback/', views.add_interview_feedback, name='add_interview_feedback'),
]

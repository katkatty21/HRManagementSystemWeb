from django.urls import path
from . import views, api

app_name = 'hrrecruitment'

urlpatterns = [
    # API Endpoints
    path('api/departments/<str:department_id>/jobs/', views.get_department_jobs, name='get_department_jobs'),
    
    # Public Job Listings
    path('', views.public_job_listings, name='careers_home'),
    path('jobs/<str:job_id>/', views.job_detail, name='job_detail'),
    path('application/<str:application_id>/success/', views.application_success, name='application_success'),
    
    # User-side Job Postings
    path('job-postings/', views.job_postings_list, name='job_postings'),
    path('submit-application/', views.submit_application, name='submit_application'),
    
    # Admin Job Management
    path('admin/jobs/', views.admin_job_postings, name='admin_job_postings'),
    path('admin/jobs/create/', views.create_job_posting, name='create_job_posting'),
    path('admin/jobs/<str:posting_id>/edit/', views.edit_job_posting, name='edit_job_posting'),
    path('admin/jobs/<str:posting_id>/delete/', views.delete_job_posting, name='delete_job_posting'),
    
    # Admin Application Management
    path('admin/applications/', views.job_applications, name='job_applications'),
    path('admin/applications/<str:application_id>/', views.application_detail, name='application_detail'),
    path('admin/applications/<str:application_id>/status/', views.update_application_status, name='update_application_status'),
    
    # Application Management
    path('admin/applications/', views.applications_list, name='applications_list'),
    path('api/applications/<str:application_id>/', views.application_detail, name='application_detail'),
    path('api/applications/<str:application_id>/status/', views.update_application_status, name='update_application_status'),
    path('applications/<str:application_id>/resume/', views.download_resume, name='download_resume'),
    
    # Interview Management
    path('admin/interviews/', views.interviews, name='interviews'),
    path('admin/applications/<str:application_id>/schedule-interview/', views.schedule_interview, name='schedule_interview'),
    path('admin/interviews/<str:interview_id>/edit/', views.edit_interview, name='edit_interview'),
    path('admin/interviews/<str:interview_id>/cancel/', views.cancel_interview, name='cancel_interview'),
    path('admin/interviews/<str:interview_id>/feedback/', views.add_interview_feedback, name='add_interview_feedback'),
    
    # Onboarding Management
    path('admin/onboarding/checklists/', views.onboarding_checklists, name='onboarding_checklists'),
    path('admin/onboarding/checklists/create/', views.create_checklist, name='create_checklist'),
    path('admin/onboarding/checklists/<str:checklist_id>/edit/', views.edit_checklist, name='edit_checklist'),
    path('admin/onboarding/checklists/<str:checklist_id>/tasks/', views.checklist_tasks, name='checklist_tasks'),
    path('admin/onboarding/checklists/<str:checklist_id>/tasks/add/', views.add_checklist_task, name='add_checklist_task'),
    path('admin/onboarding/tasks/<str:task_id>/edit/', views.edit_checklist_task, name='edit_checklist_task'),
    
    # Employee Onboarding Progress
    path('admin/onboarding/employees/', views.employee_onboarding_list, name='employee_onboarding_list'),
    path('admin/onboarding/employees/<str:employee_id>/', views.employee_onboarding_detail, name='employee_onboarding_detail'),
    path('admin/onboarding/employees/<str:employee_id>/start/', views.start_employee_onboarding, name='start_employee_onboarding'),
    path('admin/onboarding/progress/<str:progress_id>/update/', views.update_task_progress, name='update_task_progress'),
]

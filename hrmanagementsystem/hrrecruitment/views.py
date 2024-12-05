from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from hraccount.models import EmployeeInformation, Department
from .models import (
    JobPosting,
    JobApplication,
    Interview,
)
from .forms import (
    JobPostingForm,
    ApplicationStatusForm,
    InterviewForm,
    JobApplicationForm,
    InterviewFeedbackForm
)
import uuid
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound, FileResponse
from django.urls import reverse

# Recruitment Views
@login_required(login_url='login')
def job_postings(request):
    job_postings = JobPosting.objects.select_related('department', 'job').order_by('-created_at')
    return render(request, 'admin/job_postings.html', {'job_postings': job_postings})

@login_required(login_url='login')
def create_job_posting(request):
    """Create a new job posting"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            job_posting.created_by = request.user
            job_posting.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Job posting created successfully.',
                    'redirect_url': reverse('admin_job_postings')
                })
            return redirect('admin_job_postings')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobPostingForm()

    return render(request, 'admin/create_job_posting.html', {
        'form': form,
        'departments': Department.objects.all().order_by('department_name')
    })

@login_required(login_url='login')
def edit_job_posting(request, posting_id):
    posting = get_object_or_404(JobPosting, pk=posting_id)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=posting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posting updated successfully.')
            return redirect('job_postings')
    else:
        form = JobPostingForm(instance=posting)
    return render(request, 'admin/create_job_posting.html', {'form': form})

@login_required(login_url='login')
def delete_job_posting(request, posting_id):
    job_posting = get_object_or_404(JobPosting, id=posting_id)
    
    if request.method == 'POST':
        job_posting.delete()
        messages.success(request, 'Job posting deleted successfully.')
        return redirect('job_postings')
    
    return render(request, 'admin/delete_job_posting.html', {
        'job_posting': job_posting
    })

@login_required(login_url='login')
def job_applications(request):
    applications = JobApplication.objects.all().order_by('-applied_at')
    return render(request, 'admin/job_applications.html', {'applications': applications})

@login_required(login_url='login')
def application_detail(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    interviews = Interview.objects.filter(application=application)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application status updated successfully.')
            return redirect('application_detail', application_id=application.id)
    else:
        form = ApplicationStatusForm(instance=application)
    return render(request, 'admin/application_detail.html', {
        'application': application,
        'interviews': interviews,
        'form': form
    })

@login_required(login_url='login')
def schedule_interview(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            messages.success(request, 'Interview scheduled successfully.')
            return redirect('application_detail', application_id=application_id)
    else:
        form = InterviewForm()
    return render(request, 'admin/schedule_interview.html', {
        'form': form,
        'application': application
    })

@login_required(login_url='login')
def cancel_interview(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)
    if request.method == 'POST':
        interview.status = 'cancelled'
        interview.save()
        messages.success(request, 'Interview cancelled successfully.')
        return redirect('interviews')
    return render(request, 'admin/cancel_interview.html', {
        'interview': interview
    })

@login_required(login_url='login')
def add_interview_feedback(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)
    if request.method == 'POST':
        form = InterviewFeedbackForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interview feedback added successfully.')
            return redirect('interviews')
    else:
        form = InterviewFeedbackForm(instance=interview)
    return render(request, 'admin/add_interview_feedback.html', {
        'form': form,
        'interview': interview
    })

@login_required(login_url='login')
def edit_interview(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)
    if request.method == 'POST':
        form = InterviewForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interview updated successfully.')
            return redirect('interviews')
    else:
        form = InterviewForm(instance=interview)
    return render(request, 'admin/edit_interview.html', {
        'form': form,
        'interview': interview
    })

@login_required(login_url='login')
def update_application_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, 'Application status updated successfully.')
        else:
            messages.error(request, 'Invalid status value.')
    return redirect('application_detail', application_id=application.id)

@login_required(login_url='login')
def interviews(request):
    interviews = Interview.objects.all().order_by('-scheduled_at')
    return render(request, 'admin/interviews.html', {
        'interviews': interviews
    })

@login_required(login_url='login')
def job_postings_list(request):
    """View for job postings with role-based redirection"""
    if request.user.is_staff:
        return redirect('admin_job_postings')
    
    job_postings = JobPosting.objects.filter(status='OPEN').select_related('department').order_by('-created_at')
    return render(request, 'user/job_postings.html', {'job_postings': job_postings})

@login_required(login_url='login')
def admin_job_postings(request):
    """Admin view for managing job postings"""
    if not request.user.is_staff:
        return redirect('job_postings')
    
    job_postings = JobPosting.objects.all().select_related('department').order_by('-created_at')
    departments = Department.objects.all().order_by('department_name')
    return render(request, 'admin/job_postings.html', {
        'job_postings': job_postings,
        'departments': departments
    })


@login_required(login_url='login')
def submit_application(request):
    """Handle job application submission"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    job_id = request.POST.get('job_id')
    if not job_id:
        return JsonResponse({'error': 'Job ID is required'}, status=400)
        
    job = get_object_or_404(JobPosting, id=job_id)
    
    try:
        application = JobApplication.objects.create(
            job_posting=job,
            applicant=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            cover_letter=request.POST.get('cover_letter', ''),
            status='PENDING'
        )
        
        # Handle resume upload
        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            application.resume.save(
                f'resumes/{job_id}/{request.user.id}/{resume.name}',
                resume,
                save=True
            )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Application submitted successfully.',
                'redirect_url': reverse('application_success', args=[application.id])
            })
        return redirect('application_success', application_id=application.id)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# Public Views
@login_required(login_url='login')
def public_job_listings(request):
    department_id = request.GET.get('department')
    jobs = JobPosting.objects.filter(status='OPEN').select_related('department').order_by('-created_at')
    
    if department_id:
        try:
            jobs = jobs.filter(department__department_id=uuid.UUID(department_id))
        except ValueError:
            pass  # Invalid UUID format, show all jobs
    
    departments = Department.objects.filter(
        job_postings__status='OPEN'
    ).distinct()
    
    return render(request, 'public/job_listings.html', {
        'jobs': jobs,
        'departments': departments,
        'selected_department': department_id
    })

@login_required(login_url='login')
def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, status='OPEN')
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_posting = job
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('application_success', application_id=application.id)
    else:
        form = JobApplicationForm()
    
    return render(request, 'public/job_detail.html', {
        'job': job,
        'form': form
    })

def application_success(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    return render(request, 'public/application_success.html', {
        'application': application
    })

# Application Management Views
@login_required(login_url='login')
def applications_list(request):
    """View all job applications (admin only)"""
    if not request.user.is_staff:
        return redirect('job_postings')
        
    applications = JobApplication.objects.select_related(
        'job_posting', 'applicant'
    ).order_by('-created_at')
    
    return render(request, 'admin/applications.html', {
        'applications': applications
    })

@login_required(login_url='login')
def application_detail(request, application_id):
    """API endpoint for application details"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        application = JobApplication.objects.get(id=application_id)
        data = {
            'applicant_name': application.applicant.get_full_name(),
            'applicant_email': application.applicant.email,
            'job_title': application.job.title,
            'department': application.job.department.name,
            'cover_letter': application.cover_letter,
            'status': application.status,
            'created_at': application.created_at.strftime('%Y-%m-%d')
        }
        return JsonResponse(data)
    except JobApplication.DoesNotExist:
        return JsonResponse({'error': 'Application not found'}, status=404)

@login_required(login_url='login')
def update_application_status(request, application_id):
    """Update application status (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
        
    application = get_object_or_404(JobApplication, id=application_id)
    new_status = request.POST.get('status')
    
    if new_status in dict(JobApplication.STATUS_CHOICES):
        application.status = new_status
        application.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Application status updated successfully.'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid status'
    }, status=400)

@login_required(login_url='login')
def download_resume(request, application_id):
    """Download application resume"""
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    try:
        application = JobApplication.objects.get(id=application_id)
        if application.resume:
            response = FileResponse(application.resume.open(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{application.applicant.get_full_name()}_resume.pdf"'
            return response
        return HttpResponseNotFound('Resume not found')
    except JobApplication.DoesNotExist:
        return HttpResponseNotFound('Application not found')

@login_required(login_url='login')
def get_department_jobs(request, department_id):
    """API endpoint to get jobs for a specific department"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    jobs = JobPosting.objects.filter(department__department_id=department_id)
    jobs_data = [{'job_id': str(job.job_id), 'title': job.title} for job in jobs]
    return JsonResponse(jobs_data, safe=False)
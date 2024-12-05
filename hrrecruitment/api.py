from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from hraccount.models import Job, Department
from django.shortcuts import get_object_or_404

@login_required
def department_jobs(request, department_id):
    """API endpoint to get jobs for a specific department."""
    try:
        # Get department by UUID
        department = get_object_or_404(Department, department_id=department_id)
        
        # Get all jobs for the department
        jobs = Job.objects.filter(department=department).values('job_id', 'job_title')
        
        # Transform the data for the frontend
        transformed_jobs = [
            {
                'id': str(job['job_id']),  # Convert UUID to string
                'title': job['job_title']
            } 
            for job in jobs
        ]
        
        return JsonResponse(transformed_jobs, safe=False)
    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to fetch jobs. Please try again.'},
            status=400
        )

import os
import django
import sys
from datetime import date

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrmanagementsystem.settings')
django.setup()

from hraccount.models import UserAccount, Department, Job, EmployeeInformation

def create_employee_info():
    try:
        # Get or create Department and Job
        dept, _ = Department.objects.get_or_create(
            department_name="Human Resources"
        )
        job, _ = Job.objects.get_or_create(
            department=dept,
            job_title="HR Staff",
            defaults={
                'salary_range': "30000-40000",
                'job_description': "HR Staff responsibilities",
                'requirements': "Bachelor's degree in HR or related field"
            }
        )

        # Create employee information for admin
        admin = UserAccount.objects.get(email='admin@example.com')
        if not hasattr(admin, 'employee_information'):
            EmployeeInformation.objects.create(
                employee_id=admin,
                first_name=admin.first_name,
                last_name=admin.last_name,
                sex='Male',
                nationality='Filipino',
                address='123 Admin Street',
                city='Manila',
                province='Metro Manila',
                zip_code='1000',
                active_phone_number='09123456789',
                email=admin.email,
                date_hired=date.today(),
                employment_status='Regular',
                sss_number='1234567890',
                pagibig_number='1234567890',
                philhealth_number='1234567890',
                tin_number='1234567890',
                bank_account_number='1234567890',
                emergency_contact_name='Emergency Contact',
                emergency_contact_rs='Spouse',
                emergency_contact_number='09123456789',
                job=job
            )
            print("Created employee information for admin user")
        else:
            print("Admin user already has employee information")

        # Create employee information for normal user
        user = UserAccount.objects.get(email='user@example.com')
        if not hasattr(user, 'employee_information'):
            EmployeeInformation.objects.create(
                employee_id=user,
                first_name=user.first_name,
                last_name=user.last_name,
                sex='Female',
                nationality='Filipino',
                address='456 User Street',
                city='Manila',
                province='Metro Manila',
                zip_code='1000',
                active_phone_number='09987654321',
                email=user.email,
                date_hired=date.today(),
                employment_status='Regular',
                sss_number='0987654321',
                pagibig_number='0987654321',
                philhealth_number='0987654321',
                tin_number='0987654321',
                bank_account_number='0987654321',
                emergency_contact_name='Emergency Contact',
                emergency_contact_rs='Parent',
                emergency_contact_number='09987654321',
                job=job
            )
            print("Created employee information for normal user")
        else:
            print("Normal user already has employee information")

    except Exception as e:
        print(f"Error creating employee information: {str(e)}")

if __name__ == '__main__':
    create_employee_info()

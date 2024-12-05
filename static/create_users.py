import os
import django
import sys
from datetime import date

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrmanagementsystem.settings')
django.setup()

from hraccount.models import UserAccount, Department, Job, EmployeeInformation

def create_users():
    try:
        # Create Department if it doesn't exist
        dept, _ = Department.objects.get_or_create(
            department_name="Human Resources"
        )
        print("Department created/found successfully!")

        # Create Job if it doesn't exist
        job, _ = Job.objects.get_or_create(
            department=dept,
            job_title="HR Staff",
            defaults={
                'salary_range': "30000-40000",
                'job_description': "HR Staff responsibilities",
                'requirements': "Bachelor's degree in HR or related field"
            }
        )
        print("Job created/found successfully!")

        # Create admin user if doesn't exist
        admin_email = 'admin@example.com'
        if not UserAccount.objects.filter(email=admin_email).exists():
            admin = UserAccount.objects.create_user(
                email=admin_email,
                username=admin_email,
                password='admin123',
                role='Admin',
                is_staff=True,
                is_superuser=True,
                first_name='Admin',
                last_name='User'
            )
            # Create admin's employee information
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
                email=admin_email,
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
            print("Admin user and employee information created successfully!")
            print("Email: admin@example.com")
            print("Password: admin123")
        else:
            print("Admin user already exists!")

        # Create normal user if doesn't exist
        user_email = 'user@example.com'
        if not UserAccount.objects.filter(email=user_email).exists():
            user = UserAccount.objects.create_user(
                email=user_email,
                username=user_email,
                password='user123',
                role='User',
                is_staff=False,
                is_superuser=False,
                first_name='Regular',
                last_name='User'
            )
            # Create user's employee information
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
                email=user_email,
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
            print("\nNormal user and employee information created successfully!")
            print("Email: user@example.com")
            print("Password: user123")
        else:
            print("Normal user already exists!")

    except Exception as e:
        print(f"Error creating users: {str(e)}")

if __name__ == '__main__':
    create_users()

import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrmanagementsystem.settings')
django.setup()

from hraccount.models import UserAccount

def create_admin():
    try:
        # Check if admin already exists
        if UserAccount.objects.filter(email='admin@example.com').exists():
            print("Admin user already exists!")
            return

        # Create admin user
        admin = UserAccount.objects.create_user(
            email='admin@example.com',
            username='admin@example.com',
            password='admin123',
            role='Admin',
            is_staff=True,
            is_superuser=True,
            first_name='Admin',
            last_name='User'
        )
        admin.save()
        print("Admin user created successfully!")
        print("Email: admin@example.com")
        print("Password: admin123")
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")

if __name__ == '__main__':
    create_admin()

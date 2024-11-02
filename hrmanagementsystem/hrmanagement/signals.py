from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmployeeInformation, UserAccount

@receiver(post_save, sender=EmployeeInformation)
def create_or_update_user_account(sender, instance, created, **kwargs):
    # Automatically create or update UserAccount whenever EmployeeInformation is saved.
    if created:
        # Creating UserAccount for new EmployeeInformation
        UserAccount.objects.create(
            account_id=instance,  # Link to EmployeeInformation
            username=f"{instance.first_name.lower()}.{instance.last_name.lower()}",
            role=instance.role,
            password="default1234"  # Set a default password (or use a more secure approach)
        )
    else:
        # Update the UserAccount when EmployeeInformation is updated
        user_account, _ = UserAccount.objects.get_or_create(account_id=instance)
        user_account.username = f"{instance.first_name.lower()}.{instance.last_name.lower()}"
        user_account.role = instance.role
        user_account.save()

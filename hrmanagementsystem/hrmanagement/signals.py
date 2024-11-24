from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmployeeInformation, UserAccount

@receiver(post_save, sender=EmployeeInformation)
def create_or_update_user_account(sender, instance, created, **kwargs):
    """Automatically create or update UserAccount whenever EmployeeInformation is saved."""
    if created:
        # Creating UserAccount for new EmployeeInformation
        UserAccount.objects.create(
            account_id=instance,
            username=instance.email,  # Use email as username
            role=instance.role
        )
    else:
        # Update the UserAccount when EmployeeInformation is updated
        try:
            user_account = UserAccount.objects.get(account_id=instance)
            user_account.username = instance.email  # Always sync with email
            user_account.role = instance.role
            user_account.save()
        except UserAccount.DoesNotExist:
            # Create if it doesn't exist
            UserAccount.objects.create(
                account_id=instance,
                username=instance.email,
                role=instance.role
            )
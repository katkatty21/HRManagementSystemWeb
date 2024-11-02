from django.apps import AppConfig


class HrmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hrmanagement'

    def ready(self):
        import hrmanagement.signals  # Import signals to connect them

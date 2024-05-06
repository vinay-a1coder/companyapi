from django.apps import AppConfig



class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

# myapp/apps.py



class MyAppConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.signals  # Import signals when the app registry is ready

from django.apps import AppConfig

class ContactlistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contactlist"

    def ready(self):
        # Initialize ML similarity cache when app starts
        try:
            from .ml_utils import initialize_doctor_similarity
            initialize_doctor_similarity()
        except Exception:
            pass


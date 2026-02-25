from django.apps import AppConfig

class ExamibationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "examinations"

    def ready(self):
        import examinations.signals  

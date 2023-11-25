from django.apps import AppConfig


class ScholarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scholar'

    def ready(self):
        import scholar.singals

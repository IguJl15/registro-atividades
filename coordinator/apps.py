from django.apps import AppConfig


class CoordinatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coordinator'

    def ready(self):
        import coordinator.signals
from django.apps import AppConfig


class RestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rest_app'
    
    def ready(self):
        import rest_app.signals # import and connect signals here
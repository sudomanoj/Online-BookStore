from django.apps import AppConfig


class manageappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manageapp'
    
    def ready(self):
        import manageapp.signals

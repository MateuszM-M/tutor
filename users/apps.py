from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    A class to represent cofnig of learing app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """Turns on signals"""
        import users.signals

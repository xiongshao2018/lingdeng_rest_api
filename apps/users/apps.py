from django.apps import AppConfig


class RbacConfig(AppConfig):
    name = 'users'

    def ready(self):
        from .signals import create_user

from django.apps import AppConfig


class AppDbConfig(AppConfig):
    name = 'app_db'
    def ready(self):
        import app_db.signals
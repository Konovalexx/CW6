from django.apps import AppConfig

class MailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mail'

    def ready(self):
        from .tasks import start  # Импортируем функцию старта из tasks.py
        start()  # Запуск планировщика
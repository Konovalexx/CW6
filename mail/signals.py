from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def start_sending_mailing(sender, **kwargs):
    print("Запуск отправки рассылки")  # Для отладки
    from .tasks import start  # Измените импорт на tasks
    start()  # Запускаем задачи рассылки после миграции
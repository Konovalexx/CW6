from django.db import models
from django.conf import settings

class Client(models.Model):
    email = models.EmailField()  # Убрали unique=True
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='clients')

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subject', 'owner')  # Уникальность по subject и owner

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('finished', 'Завершена'),
    )

    FREQUENCY_CHOICES = (
        ('daily', 'Ежедневная'),
        ('weekly', 'Еженедельная'),
        ('monthly', 'Ежемесячная'),
    )

    start_time = models.DateTimeField()
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, related_name='mailings')  # Добавлен related_name для обратной связи
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Рассылка {self.id} от {self.owner}"

    class Meta:
        permissions = [
            ("can_view_any_mailing", "Может просматривать любые рассылки"),
            ("can_disable_mailings", "Может отключать рассылки"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = (
        ('successful', 'Успешно'),
        ('failed', 'Не успешно'),
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    response = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # Сделали owner допускающим null

    def __str__(self):
        return f"Попытка рассылки {self.mailing.id} - {self.status} ({self.timestamp})"

    # Метод для фильтрации попыток рассылок по пользователю
    @staticmethod
    def get_user_attempts(user):
        return MailingAttempt.objects.filter(owner=user).order_by('-timestamp')
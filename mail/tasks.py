from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .models import Mailing, MailingAttempt
import pytz
import smtplib
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

def start():
    """
    Инициализация и запуск фонового планировщика для отправки рассылок.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=60)  # Настройте интервал по необходимости
    scheduler.start()
    logger.info("Scheduler started and mail sending job added.")

def send_mailing():
    """
    Функция для отправки активных рассылок.
    Проверяет, какие рассылки следует отправить и обрабатывает их.
    """
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = timezone.now()

    # Получаем все активные рассылки, которые должны быть отправлены
    mailings = Mailing.objects.filter(start_time__lte=current_datetime, status='running')

    logger.info(f"Found {len(mailings)} mailings to process.")

    for mailing in mailings:
        # Проверка последней попытки отправки
        last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-timestamp').first()
        if last_attempt:
            # Логика проверки частоты отправки
            if not check_frequency(last_attempt, mailing.frequency):
                logger.info(f"Skipping mailing {mailing.id} due to frequency check.")
                continue

        try:
            # Отправка почты
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()],
                fail_silently=False,
            )
            MailingAttempt.objects.create(mailing=mailing, status='successful')
            logger.info(f'Successfully sent mailing: {mailing.id}')  # Логирование успешной отправки
        except smtplib.SMTPException as e:
            MailingAttempt.objects.create(mailing=mailing, status='failed', response=str(e))
            logger.error(f'Failed to send mailing {mailing.id}: {str(e)}')  # Логирование ошибки SMTP
        except Exception as e:  # Обработка других возможных исключений
            MailingAttempt.objects.create(mailing=mailing, status='failed', response=str(e))
            logger.error(f'Error sending mailing {mailing.id}: {str(e)}')  # Логирование общей ошибки

def check_frequency(last_attempt, frequency):
    """
    Проверка, прошел ли необходимый интервал времени с последней попытки отправки.
    """
    interval_mapping = {
        'daily': timezone.timedelta(days=1),
        'weekly': timezone.timedelta(weeks=1),
        'monthly': timezone.timedelta(weeks=4),
    }
    last_attempt_time_local = last_attempt.timestamp.astimezone(pytz.timezone(settings.TIME_ZONE))

    # Расчет ожидаемого времени следующей отправки
    expected_next_attempt_time = last_attempt_time_local + interval_mapping.get(frequency, timezone.timedelta(days=1))

    logger.info(f"Current time: {timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))}, "
                f"Last attempt time: {last_attempt_time_local}, "
                f"Expected next attempt time: {expected_next_attempt_time}")

    is_frequency_ok = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE)) >= expected_next_attempt_time

    if not is_frequency_ok:
        logger.info(f"Mailing frequency not met for {last_attempt.mailing.id}. Last attempt: {last_attempt_time_local}")

    return is_frequency_ok
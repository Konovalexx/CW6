from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email_verified', True)  # Суперпользователь не требует подтверждения email

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Страна",
    )
    email_verified = models.BooleanField(default=False, verbose_name="Email верифицирован")
    email_verification_token = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name="Токен для верификации email",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def send_verification_email(self):
        verification_link = f"{settings.SITE_URL}/users/verify-email/{self.pk}/{self.email_verification_token}/"
        send_mail(
            'Подтвердите ваш email',
            f'Пожалуйста, подтвердите ваш email, перейдя по следующей ссылке: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
        )

    def generate_verification_token(self):
        token = get_random_string(32)
        self.email_verification_token = token
        self.save()  # Сохраняем токен в базе данных
        return token
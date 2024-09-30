from django.db import models
from django.utils.text import slugify
from django.db import connection
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils import timezone  # Импортируем для работы с временными метками


class Category(models.Model):
    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')

    name = models.CharField(
        max_length=150,
        verbose_name="Категория",
        help_text="Введите название категории:",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории:",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Введите заголовок статьи:",
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL-метка",
        help_text="Введите URL-метку статьи:",
        null=True,
    )
    content = models.TextField(
        default='',
        verbose_name="Содержимое",
        help_text="Введите текст статьи:",
    )
    preview = models.ImageField(
        upload_to="catalog/previews",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение превью статьи:",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата публикации")  # Новое поле
    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Выберите категорию статьи:",
        blank=True,
        null=True,
        related_name="products",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name="Создатель",
        null=True,
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)

        # Устанавливаем дату публикации, если товар опубликован
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()  # Устанавливаем текущую дату и время
        elif not self.is_published:
            self.published_at = None  # Очищаем дату публикации, если статья не опубликована

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
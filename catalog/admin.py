from django.contrib import admin
from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "category", "is_published", "views_count", "created_at")
    search_fields = ("title", "content")
    list_filter = ("category", "is_published")
    prepopulated_fields = {"slug": ("title",)}

    def get_readonly_fields(self, request, obj=None):
        # Поле slug будет редактируемым только для пользователей с правом изменения описания
        if request.user.has_perm('catalog.can_change_product_description') or request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return ('slug',)  # Поле slug будет только для чтения для остальных пользователей
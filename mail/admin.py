from django.contrib import admin
from .models import Mailing, Client, Message, MailingAttempt

class MailingAttemptInline(admin.TabularInline):
    model = MailingAttempt
    extra = 0

class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'frequency', 'status', 'owner')
    search_fields = ('status', 'owner__username')
    inlines = [MailingAttemptInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)  # Фильтруем рассылки по владельцу

class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)  # Фильтруем сообщения по владельцу

class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'status', 'timestamp', 'response')
    list_filter = ('status',)
    search_fields = ('mailing__id', 'response')

# Регистрация моделей в админке
admin.site.register(Mailing, MailingAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MailingAttempt, MailingAttemptAdmin)
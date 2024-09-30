from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('mailings/', views.mailing_list, name='mailing_list'),  # Список рассылок
    path('mailings/create/', views.mailing_create, name='mailing_create'),  # Создание рассылки
    path('mailings/<int:pk>/update/', views.mailing_update, name='mailing_update'),  # Обновление рассылки
    path('mailings/<int:pk>/delete/', views.mailing_delete, name='mailing_delete'),  # Удаление рассылки
    path('clients/', views.client_list, name='client_list'),  # Список клиентов
    path('clients/create/', views.client_create, name='client_create'),  # Создание клиента
    path('clients/<int:pk>/update/', views.client_update, name='client_update'),  # Обновление клиента
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),  # Удаление клиента
    path('messages/', views.message_list, name='message_list'),  # Список сообщений
    path('messages/create/', views.message_create, name='message_create'),  # Создание сообщения
    path('messages/<int:pk>/update/', views.message_update, name='message_update'),  # Обновление сообщения
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),  # Удаление сообщения
    path('home/', views.mailing_home, name='mailing_home'),  # Главная страница рассылок
    path('mailing-report/', views.mailing_report, name='mailing_report'),  # Отчёт по рассылкам
]
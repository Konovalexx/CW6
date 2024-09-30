from django.shortcuts import render, redirect, get_object_or_404
from .models import Mailing, Client, Message, MailingAttempt
from .forms import MailingForm, ClientForm, MessageForm
from django.contrib.auth.decorators import login_required


# Главная страница
def home(request):
    return render(request, 'home.html')


# Главная страница рассылок
@login_required
def mailing_home(request):
    return render(request, 'mail/mailing_home.html')


# Mailing views
@login_required
def mailing_list(request):
    mailings = Mailing.objects.filter(owner=request.user)
    return render(request, 'mail/mailing_list.html', {'mailings': mailings})


@login_required
def mailing_create(request):
    if request.method == 'POST':
        form = MailingForm(request.POST, owner=request.user)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user
            mailing.save()
            form.save_m2m()  # Сохраняем связи ManyToMany
            return redirect('mail:mailing_list')
    else:
        form = MailingForm(owner=request.user)
    return render(request, 'mail/mailing_form.html', {'form': form})


@login_required
def mailing_update(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing, owner=request.user)
        if form.is_valid():
            form.save()
            return redirect('mail:mailing_list')
    else:
        form = MailingForm(instance=mailing, owner=request.user)
    return render(request, 'mail/mailing_form.html', {'form': form})


@login_required
def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
    if request.method == 'POST':
        mailing.delete()
        return redirect('mail:mailing_list')
    return render(request, 'mail/mailing_confirm_delete.html', {'mailing': mailing})


# Отчет о попытках рассылок
@login_required
def mailing_report(request):
    # Получаем все попытки рассылок текущего пользователя
    attempts = MailingAttempt.objects.filter(mailing__owner=request.user).order_by('-timestamp')

    # Получаем общее количество рассылок
    total_mailings = Mailing.objects.filter(owner=request.user).count()

    # Получаем количество активных рассылок
    active_mailings = Mailing.objects.filter(owner=request.user, status='running').count()

    # Получаем количество уникальных клиентов для рассылок
    unique_clients = Client.objects.filter(owners=request.user).distinct().count()

    # Проверка на наличие попыток
    if not attempts:
        message = "Нет данных о попытках рассылок."
    else:
        message = None

    return render(request, 'mail/mailing_report.html', {
        'attempts': attempts,
        'message': message,
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
    })


# Client views
@login_required
def client_list(request):
    clients = Client.objects.filter(owners=request.user)
    return render(request, 'mail/client_list.html', {'clients': clients})


@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            client.owners.add(request.user)
            return redirect('mail:client_list')
    else:
        form = ClientForm()
    return render(request, 'mail/client_form.html', {'form': form})


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk, owners=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('mail:client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'mail/client_form.html', {'form': form})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, owners=request.user)
    if request.method == 'POST':
        client.delete()
        return redirect('mail:client_list')
    return render(request, 'mail/client_confirm_delete.html', {'client': client})


# Message views
@login_required
def message_list(request):
    messages = Message.objects.filter(owner=request.user)
    return render(request, 'mail/message_list.html', {'messages': messages})


@login_required
def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.owner = request.user
            message.save()
            return redirect('mail:message_list')
    else:
        form = MessageForm()
    return render(request, 'mail/message_form.html', {'form': form})


@login_required
def message_update(request, pk):
    message = get_object_or_404(Message, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('mail:message_list')
    else:
        form = MessageForm(instance=message)
    return render(request, 'mail/message_form.html', {'form': form})


@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk, owner=request.user)
    if request.method == 'POST':
        message.delete()
        return redirect('mail:message_list')
    return render(request, 'mail/message_confirm_delete.html', {'message': message})
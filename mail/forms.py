from django import forms
from .models import Mailing, Client, Message

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'frequency', 'status', 'message', 'clients']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)  # Получаем владельца, если передан
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.none()  # Изначально пустой queryset для клиентов

        if owner:
            # Показываем только клиентов и сообщения, принадлежащие текущему владельцу
            self.fields['clients'].queryset = Client.objects.filter(owners=owner)
            self.fields['message'].queryset = Message.objects.filter(owner=owner)

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get('frequency')

        # Проверка допустимой частоты рассылки
        if frequency not in dict(self.fields['frequency'].choices):
            self.add_error('frequency', "Выберите допустимую частоту.")

        # Проверка наличия сообщения
        if not cleaned_data.get('message'):
            self.add_error('message', "Необходимо выбрать сообщение.")

        return cleaned_data


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Введите email', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Введите полное имя', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Введите комментарий', 'rows': 4, 'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Введите email.")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name:
            raise forms.ValidationError("Введите полное имя.")
        return full_name


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Введите тему сообщения', 'class': 'form-control'}),
            'body': forms.Textarea(
                attrs={'placeholder': 'Введите текст сообщения', 'rows': 6, 'class': 'form-control'}),
        }

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if not subject:
            raise forms.ValidationError("Тема сообщения не может быть пустой.")
        return subject

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if not body:
            raise forms.ValidationError("Текст сообщения не может быть пустым.")
        return body
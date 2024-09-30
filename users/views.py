from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    LogoutView as AuthLogoutView,
    PasswordResetView as AuthPasswordResetView,
    PasswordResetConfirmView as AuthPasswordResetConfirmView,
)
from django.views.generic import CreateView, View
from .models import CustomUser
from .forms import CustomUserCreationForm, PasswordResetForm, CustomAuthenticationForm

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.generate_verification_token()
        user.send_verification_email()
        return super().form_valid(form)

class EmailVerificationView(View):
    def get(self, request, user_id, token):
        user = get_object_or_404(CustomUser, pk=user_id)
        if user.email_verification_token == token:
            user.email_verified = True
            user.email_verification_token = ""
            user.save()
            return render(request, 'users/email_verified.html')
        else:
            return render(request, 'users/email_verification_failed.html')

class CustomPasswordResetView(AuthPasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

class CustomPasswordResetConfirmView(AuthPasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')

class LoginView(AuthLoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm

class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('catalog:index')
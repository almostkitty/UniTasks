from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма регистрации без help_text на русском языке"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем русские метки и убираем help_text
        if 'username' in self.fields:
            self.fields['username'].label = 'Имя пользователя'
            self.fields['username'].help_text = None
            self.fields['username'].widget.attrs.update({'placeholder': 'Введите имя пользователя'})
        if 'password1' in self.fields:
            self.fields['password1'].label = 'Пароль'
            self.fields['password1'].help_text = None
            self.fields['password1'].widget.attrs.update({'placeholder': 'Введите пароль'})
        if 'password2' in self.fields:
            self.fields['password2'].label = 'Подтверждение пароля'
            self.fields['password2'].help_text = None
            self.fields['password2'].widget.attrs.update({'placeholder': 'Подтвердите пароль'})
    
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    """Кастомная форма входа без help_text на русском языке"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем русские метки и убираем help_text
        if 'username' in self.fields:
            self.fields['username'].label = 'Имя пользователя'
            self.fields['username'].help_text = None
            self.fields['username'].widget.attrs.update({'placeholder': 'Введите имя пользователя', 'autofocus': True})
        if 'password' in self.fields:
            self.fields['password'].label = 'Пароль'
            self.fields['password'].help_text = None
            self.fields['password'].widget.attrs.update({'placeholder': 'Введите пароль'})


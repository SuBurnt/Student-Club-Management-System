from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'student_id', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер студенческого билета'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
        }

from django import forms
from .models import Club


class ClubForm(forms.ModelForm):
    """Форма для создания и редактирования клуба."""

    class Meta:
        model = Club
        fields = ['name', 'description', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название клуба'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание клуба',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

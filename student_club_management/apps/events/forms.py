from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    """Форма для создания мероприятия."""
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time', 'location', 'max_participants']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название мероприятия'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание мероприятия',
                'rows': 4
            }),
            'date_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Место проведения'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
        }
from django import forms
from .models import DiscussionTopic, Comment


class DiscussionTopicForm(forms.ModelForm):
    """Форма для создания темы обсуждения."""
    
    class Meta:
        model = DiscussionTopic
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок темы'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Содержание темы',
                'rows': 6
            }),
        }


class CommentForm(forms.ModelForm):
    """Форма для добавления комментария."""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш комментарий',
                'rows': 3
            }),
        }
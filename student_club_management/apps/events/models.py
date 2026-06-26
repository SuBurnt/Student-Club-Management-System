from django.db import models
from django.conf import settings
from apps.clubs.models import Club


class Event(models.Model):
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    max_participants = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_registered_count(self):
        return self.registrations.filter(status='confirmed').count()

    def __str__(self):
        return f"{self.title} ({self.date_time})"


class EventRegistration(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено')
    ], default='pending')

    class Meta:
        unique_together = ['event', 'user']

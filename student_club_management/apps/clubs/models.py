from django.db import models
from django.conf import settings


class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('sport', 'Спорт'),
        ('art', 'Искусство'),
        ('science', 'Наука'),
        ('tech', 'Технологии'),
        ('other', 'Другое')
    ])
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_clubs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ClubMember',
        related_name='clubs'
    )

    class Meta:
        verbose_name_plural = "Clubs"

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Администратор'),
        ('member', 'Участник')
    ], default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'club']

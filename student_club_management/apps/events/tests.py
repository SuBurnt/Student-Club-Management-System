from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.clubs.models import Club
from apps.events.models import Event, EventRegistration
from django.contrib.auth import get_user_model

User = get_user_model()

class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            student_id='STU001'
        )
        self.club = Club.objects.create(
            name='Test Club',
            description='Test',
            category='tech',
            owner=self.user
        )
        self.event = Event.objects.create(
            club=self.club,
            title='Workshop',
            description='Python workshop',
            date_time=timezone.now() + timedelta(days=7),
            location='Room 101',
            max_participants=20
        )
    
    def test_event_creation(self):
        """Тест создания мероприятия"""
        self.assertEqual(self.event.title, 'Workshop')
        self.assertEqual(self.event.max_participants, 20)
    
    def test_get_registered_count(self):
        """Тест подсчёта зарегистрированных"""
        self.assertEqual(self.event.get_registered_count(), 0)
        
        EventRegistration.objects.create(
            event=self.event,
            user=self.user,
            status='confirmed'
        )
        
        self.assertEqual(self.event.get_registered_count(), 1)
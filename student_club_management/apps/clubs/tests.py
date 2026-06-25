from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.clubs.models import Club, ClubMember

User = get_user_model()

class ClubModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            student_id='STU001'
        )
        self.club = Club.objects.create(
            name='Programming Club',
            description='Club for programmers',
            category='tech',
            owner=self.user
        )
    
    def test_club_creation(self):
        """Тест создания клуба"""
        self.assertEqual(self.club.name, 'Programming Club')
        self.assertEqual(self.club.category, 'tech')
        self.assertIsNotNone(self.club.created_at)
    
    def test_club_str(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.club), 'Programming Club')
    
    def test_club_member_creation(self):
        """Тест создания члена клуба"""
        member = ClubMember.objects.create(
            user=self.user,
            club=self.club,
            role='admin'
        )
        self.assertEqual(member.role, 'admin')
        self.assertIn(member, self.club.clubmember_set.all())
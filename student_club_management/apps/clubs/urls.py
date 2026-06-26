from django.urls import path
from . import views

app_name = 'clubs'

urlpatterns = [
    path('', views.club_list, name='club_list'),
    path('<int:club_id>/', views.club_detail, name='club_detail'),
    path('create/', views.create_club, name='create_club'),
    path('<int:club_id>/join/', views.join_club, name='join_club'),
    path('<int:club_id>/delete/', views.delete_club, name='delete_club'),
]

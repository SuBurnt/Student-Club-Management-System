from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('club/<int:club_id>/', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('club/<int:club_id>/create/', views.create_event, name='create_event'),
]
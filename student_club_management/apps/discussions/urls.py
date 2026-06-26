from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path(
        'club/<int:club_id>/',
        views.topic_list,
        name='topic_list'),
    path(
        'topic/<int:topic_id>/',
        views.topic_detail,
        name='topic_detail'),
    path(
        'club/<int:club_id>/create/',
        views.create_topic,
        name='create_topic'),
    path(
        'topic/<int:topic_id>/delete/',
        views.delete_topic,
        name='delete_topic'),
    path(
        'comment/<int:comment_id>/delete/',
        views.delete_comment,
        name='delete_comment'),
]

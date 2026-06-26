from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import DiscussionTopic, Comment
from .forms import DiscussionTopicForm, CommentForm


def topic_list(request, club_id):
    """Список тем обсуждений в клубе."""
    from apps.clubs.models import Club
    club = get_object_or_404(Club, id=club_id)
    topics = DiscussionTopic.objects.filter(club=club).order_by('-created_at')
    return render(request, 'discussions/topic_list.html', {
        'club': club,
        'topics': topics
    })


def topic_detail(request, topic_id):
    """Просмотр темы и комментариев."""
    topic = get_object_or_404(DiscussionTopic, id=topic_id)
    comments = Comment.objects.filter(topic=topic).select_related('user')

    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.topic = topic
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('discussions:topic_detail', topic_id=topic.id)

    return render(request, 'discussions/topic_detail.html', {
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form
    })


@login_required
def create_topic(request, club_id):
    """Создание новой темы обсуждения."""
    from apps.clubs.models import Club
    club = get_object_or_404(Club, id=club_id)

    if request.method == 'POST':
        form = DiscussionTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.club = club
            topic.created_by = request.user
            topic.save()
            messages.success(request, 'Тема создана!')
            return redirect('discussions:topic_detail', topic_id=topic.id)
    else:
        form = DiscussionTopicForm()

    return render(request, 'discussions/create_topic.html', {
        'form': form,
        'club': club
    })


@staff_member_required
def delete_topic(request, topic_id):
    """Удаление темы обсуждения (только для суперюзера)."""
    topic = get_object_or_404(DiscussionTopic, id=topic_id)
    club_id = topic.club.id

    if request.method == 'POST':
        topic_title = topic.title
        topic.delete()
        messages.success(request, f'Тема "{topic_title}" удалена.')
        return redirect('discussions:topic_list', club_id=club_id)

    return render(request, 'discussions/delete_topic.html', {'topic': topic})


@staff_member_required
def delete_comment(request, comment_id):
    """Удаление комментария (только для суперюзера)."""
    comment = get_object_or_404(Comment, id=comment_id)
    topic_id = comment.topic.id

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий удалён.')
        return redirect('discussions:topic_detail', topic_id=topic_id)

    return render(request,
                  'discussions/delete_comment.html',
                  {'comment': comment})

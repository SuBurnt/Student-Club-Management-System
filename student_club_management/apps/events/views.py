from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.clubs.models import Club
from .models import Event, EventRegistration
from .forms import EventForm


def event_list(request, club_id):
    """Список мероприятий клуба"""
    club = get_object_or_404(Club, id=club_id)
    events = club.events.filter(date_time__gte=timezone.now())
    return render(request, 'events/event_list.html', {
        'club': club,
        'events': events
    })


def event_detail(request, event_id):
    """Детали мероприятия."""
    event = get_object_or_404(Event, id=event_id)
    registrations = event.registrations.filter(
        status='confirmed').select_related('user')
    is_registered = False
    if request.user.is_authenticated:
        is_registered = event.registrations.filter(
            user=request.user,
            status='confirmed'
        ).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'participants': registrations,
        'is_registered': is_registered
    })


@login_required
def register_for_event(request, event_id):
    """Регистрация на мероприятие"""
    event = get_object_or_404(Event, id=event_id)

    if event.get_registered_count() >= event.max_participants:
        messages.error(request, 'Мероприятие заполнено!')
        return redirect('events:event_detail', event_id=event.id)

    registration, created = EventRegistration.objects.get_or_create(
        event=event,
        user=request.user,
        defaults={'status': 'confirmed'}
    )

    if created:
        messages.success(request, f'Вы зарегистрированы на "{event.title}"')
    else:
        messages.info(request, 'Вы уже зарегистрированы на это мероприятие')

    return redirect('events:event_detail', event_id=event.id)


@login_required
def create_event(request, club_id):
    """Создание мероприятия (только для админов клуба)"""
    club = get_object_or_404(Club, id=club_id)

    if not club.clubmember_set.filter(
        user=request.user,
        role='admin'
    ).exists():
        messages.error(
            request,
            'Только администраторы могут создавать мероприятия')
        return redirect('clubs:club_detail', club_id=club.id)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.save()
            messages.success(request, 'Мероприятие создано!')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {
        'form': form,
        'club': club
    })

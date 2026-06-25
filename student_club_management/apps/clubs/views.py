from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Club, ClubMember
from .forms import ClubForm

def club_list(request):
    """Список всех клубов"""
    clubs = Club.objects.all()
    category = request.GET.get('category')
    if category:
        clubs = clubs.filter(category=category)
    return render(request, 'clubs/club_list.html', {'clubs': clubs})

def club_detail(request, club_id):
    """Детальная информация о клубе"""
    club = get_object_or_404(Club, id=club_id)
    members = club.clubmember_set.all()
    is_member = False
    if request.user.is_authenticated:
        is_member = club.members.filter(id=request.user.id).exists()
    return render(request, 'clubs/club_detail.html', {
        'club': club,
        'members': members,
        'is_member': is_member
    })

@login_required
def join_club(request, club_id):
    """Присоединиться к клубу"""
    club = get_object_or_404(Club, id=club_id)
    if not club.members.filter(id=request.user.id).exists():
        ClubMember.objects.create(
            user=request.user,
            club=club,
            role='member'
        )
        messages.success(request, f'Вы присоединились к клубу "{club.name}"')
    return redirect('clubs:club_detail', club_id=club.id)

@login_required
def create_club(request):
    """Создание нового клуба"""
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.owner = request.user
            club.save()
            ClubMember.objects.create(
                user=request.user,
                club=club,
                role='admin'
            )
            messages.success(request, 'Клуб успешно создан!')
            return redirect('clubs:club_detail', club_id=club.id)
    else:
        form = ClubForm()
    return render(request, 'clubs/create_club.html', {'form': form})

@staff_member_required
def delete_club(request, club_id):
    """Удаление клуба (только для суперюзера)."""
    club = get_object_or_404(Club, id=club_id)
    
    if request.method == 'POST':
        club_name = club.name
        club.delete()
        messages.success(request, f'Клуб "{club_name}" удалён.')
        return redirect('clubs:club_list')
    
    return render(request, 'clubs/delete_club.html', {'club': club})
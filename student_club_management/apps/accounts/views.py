from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm


def register_view(request):
    """Регистрация нового студента."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('clubs:club_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Вход в систему."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f'Добро пожаловать, {
                    user.first_name or user.username}!')
            return redirect('clubs:club_list')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Выход из системы."""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """Просмотр профиля студента."""
    user = request.user
    clubs = user.clubs.all()  # Через related_name в модели
    return render(request, 'accounts/profile.html', {
        'user': user,
        'clubs': clubs
    })

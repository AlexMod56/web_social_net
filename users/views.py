from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserRegisterForm, UserLoginForm
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/profile.html', {'user': user, 'form': form, 'profile': profile})

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})

def user_list_view(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def profile_read_only_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = UserProfile.objects.get(user=user)
    return render(request, 'users/profile_read_only.html', {'user': user, 'profile': profile})

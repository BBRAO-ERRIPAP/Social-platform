from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from friends.models import Follow, FriendRequest


def register(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}!')
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'feed'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.post_set.all().order_by('-created_at')
    is_following = Follow.objects.filter(
        follower=request.user, following=profile_user
    ).exists()
    friend_request_sent = FriendRequest.objects.filter(
        sender=request.user, receiver=profile_user, status='pending'
    ).exists()
    friend_request_received = FriendRequest.objects.filter(
        sender=profile_user, receiver=request.user, status='pending'
    ).first()
    are_friends = FriendRequest.objects.filter(
        Q(sender=request.user, receiver=profile_user) |
        Q(sender=profile_user, receiver=request.user),
        status='accepted'
    ).exists()
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
        'are_friends': are_friends,
    })


@login_required
def edit_profile(request,username):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def search_users(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)
    return render(request, 'users/search.html', {'results': results, 'query': query})


@login_required
def suggested_users(request):
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following_id', flat=True)
    suggestions = User.objects.exclude(
        id__in=list(following_ids) + [request.user.id]
    ).order_by('?')[:10]
    return render(request, 'users/suggested.html', {'suggestions': suggestions})
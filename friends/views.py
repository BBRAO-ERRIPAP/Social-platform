from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from notifications.models import Notification
from .models import Follow, FriendRequest


@login_required
@require_POST
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect('profile', username=username)
    follow, created = Follow.objects.get_or_create(
        follower=request.user, following=target
    )
    if not created:
        follow.delete()
        messages.info(request, f'You unfollowed {target.username}.')
    else:
        messages.success(request, f'You are now following {target.username}.')
        Notification.objects.create(
            recipient=target,
            sender=request.user,
            notification_type='follow',
        )
    return redirect('profile', username=username)


@login_required
@require_POST
def send_friend_request(request, username):
    receiver = get_object_or_404(User, username=username)
    if receiver == request.user:
        messages.error(request, "You cannot send a request to yourself.")
        return redirect('profile', username=username)
    fr, created = FriendRequest.objects.get_or_create(
        sender=request.user, receiver=receiver
    )
    if created:
        messages.success(request, f'Friend request sent to {receiver.username}.')
        Notification.objects.create(
            recipient=receiver,
            sender=request.user,
            notification_type='friend_request',
        )
    else:
        messages.info(request, 'Friend request already sent.')
    return redirect('profile', username=username)


@login_required
@require_POST
def respond_friend_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    action = request.POST.get('action')
    if action == 'accept':
        fr.status = 'accepted'
        fr.save()
        messages.success(request, f'You are now friends with {fr.sender.username}.')
        Notification.objects.create(
            recipient=fr.sender,
            sender=request.user,
            notification_type='friend_accept',
        )
    elif action == 'decline':
        fr.status = 'declined'
        fr.save()
        messages.info(request, 'Friend request declined.')
    return redirect('notifications_list')


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user).select_related('follower')
    return render(request, 'friends/followers.html', {
        'profile_user': user,
        'followers': followers,
    })


@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user).select_related('following')
    return render(request, 'friends/following.html', {
        'profile_user': user,
        'following': following,
    })


@login_required
def friends_list(request):
    from django.db.models import Q
    accepted = FriendRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status='accepted'
    ).select_related('sender', 'receiver')
    friends = []
    for fr in accepted:
        friends.append(fr.receiver if fr.sender == request.user else fr.sender)
    pending = FriendRequest.objects.filter(receiver=request.user, status='pending')
    return render(request, 'friends/friends_list.html', {
        'friends': friends,
        'pending_requests': pending,
    })
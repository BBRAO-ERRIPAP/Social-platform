from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from friends.models import Follow
from notifications.models import Notification
from .models import Post, Comment
from .forms import PostForm, CommentForm


@login_required
def feed(request):
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following_id', flat=True)
    posts = Post.objects.filter(
        author_id__in=list(following_ids) + [request.user.id]
    ).select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    suggestions = User.objects.exclude(
        id__in=list(following_ids) + [request.user.id]
    ).order_by('?')[:5]
    return render(request, 'posts/feed.html', {
        'posts': posts,
        'post_form': PostForm(),
        'suggestions': suggestions,
    })


@login_required
@require_POST
def create_post(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, 'Post created!')
    else:
        messages.error(request, 'Could not create post.')
    return redirect('feed')


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comment_form': CommentForm(),
    })


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('feed')


@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        if post.author != request.user:
            Notification.objects.get_or_create(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                post=post,
            )
    return JsonResponse({'liked': liked, 'count': post.like_count()})


@login_required
@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        if post.author != request.user:
            Notification.objects.get_or_create(
                recipient=post.author,
                sender=request.user,
                notification_type='comment',
                post=post,
            )
    return redirect('post_detail', pk=pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
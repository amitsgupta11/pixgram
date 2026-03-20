from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import (Post, Like, Comment, SavedPost,
                     Notification, Story, StoryView, DirectMessage)
from .forms import PostForm, CommentForm, StoryForm
from accounts.models import Follow


def landing(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'posts/landing.html')


@login_required
def feed(request):
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following_id', flat=True)
    all_ids = list(following_ids) + [request.user.id]

    posts = Post.objects.filter(
        author_id__in=all_ids
    ).select_related('author', 'author__profile').prefetch_related('likes', 'comments')

    if not posts.exists():
        posts = Post.objects.select_related(
            'author', 'author__profile'
        ).prefetch_related('likes', 'comments').all()

    liked_post_ids = set(Like.objects.filter(
        user=request.user).values_list('post_id', flat=True))
    saved_post_ids = set(SavedPost.objects.filter(
        user=request.user).values_list('post_id', flat=True))
    unread_notif_count = Notification.objects.filter(
        recipient=request.user, is_read=False).count()
    unread_dm_count = DirectMessage.objects.filter(
        receiver=request.user, is_read=False).count()

    # Active stories from following
    cutoff = timezone.now() - timedelta(hours=24)
    stories = Story.objects.filter(
        author_id__in=all_ids,
        created_at__gte=cutoff
    ).select_related('author', 'author__profile').order_by('author_id', '-created_at')

    # Ek user ka sirf latest story
    seen_authors = set()
    unique_stories = []
    for s in stories:
        if s.author_id not in seen_authors:
            seen_authors.add(s.author_id)
            unique_stories.append(s)

    return render(request, 'posts/feed.html', {
        'posts':              posts,
        'liked_post_ids':     liked_post_ids,
        'saved_post_ids':     saved_post_ids,
        'unread_notif_count': unread_notif_count,
        'unread_dm_count':    unread_dm_count,
        'stories':            unique_stories,
        'comment_form':       CommentForm(),
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post shared! ✨')
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_detail(request, pk):
    post         = get_object_or_404(Post, pk=pk)
    comments     = post.comments.select_related('user', 'user__profile').all()
    liked        = Like.objects.filter(user=request.user, post=post).exists()
    saved        = SavedPost.objects.filter(user=request.user, post=post).exists()
    return render(request, 'posts/post_detail.html', {
        'post': post, 'comments': comments,
        'liked': liked, 'saved': saved,
        'comment_form': CommentForm(),
    })


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "Aap doosre ka post edit nahi kar sakte.")
        return redirect('feed')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('feed')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('feed')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('feed')
    return render(request, 'posts/confirm_delete.html', {'post': post})


@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    else:
        if post.author != request.user:
            Notification.objects.get_or_create(
                recipient=post.author, sender=request.user,
                notif_type='like', post=post)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': created, 'count': post.like_count})
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.post = post
            c.save()
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author, sender=request.user,
                    notif_type='comment', post=post)
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
def toggle_save(request, pk):
    post = get_object_or_404(Post, pk=pk)
    obj, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    if not created:
        obj.delete()
        messages.info(request, 'Post unsaved.')
    else:
        messages.success(request, 'Post saved! 🔖')
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
def saved_posts(request):
    saved = SavedPost.objects.filter(
        user=request.user
    ).select_related('post', 'post__author', 'post__author__profile')
    return render(request, 'posts/saved_posts.html', {'saved': saved})


@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(
        recipient=request.user
    ).select_related('sender', 'sender__profile', 'post')[:50]
    Notification.objects.filter(
        recipient=request.user, is_read=False).update(is_read=True)
    return render(request, 'posts/notifications.html', {'notifs': notifs})


@login_required
def explore_view(request):
    following_ids = list(Follow.objects.filter(
        follower=request.user).values_list('following_id', flat=True))
    following_ids.append(request.user.id)

    trending_posts = Post.objects.annotate(
        total_likes=Count('likes')
    ).order_by('-total_likes', '-created_at')[:12]

    suggested_users = User.objects.exclude(
        id__in=following_ids
    ).annotate(
        followers_count=Count('follower_set')
    ).order_by('-followers_count').select_related('profile')[:8]

    liked_post_ids = set(Like.objects.filter(
        user=request.user).values_list('post_id', flat=True))
    saved_post_ids = set(SavedPost.objects.filter(
        user=request.user).values_list('post_id', flat=True))

    return render(request, 'posts/explore.html', {
        'trending_posts':  trending_posts,
        'suggested_users': suggested_users,
        'liked_post_ids':  liked_post_ids,
        'saved_post_ids':  saved_post_ids,
    })


# ═══════════════════════════════════════════════
# STORIES
# ═══════════════════════════════════════════════

@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            messages.success(request, 'Story added! Visible for 24 hours.')
            return redirect('feed')
    else:
        form = StoryForm()
    return render(request, 'stories/create_story.html', {'form': form})


@login_required
def view_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if not story.is_active:
        messages.error(request, 'Yeh story expire ho gayi.')
        return redirect('feed')
    # View record karo
    StoryView.objects.get_or_create(story=story, viewer=request.user)

    # Same author ki saari active stories
    cutoff = timezone.now() - timedelta(hours=24)
    author_stories = Story.objects.filter(
        author=story.author,
        created_at__gte=cutoff
    ).order_by('created_at')

    # Next story
    next_story = author_stories.filter(created_at__gt=story.created_at).first()

    return render(request, 'stories/view_story.html', {
        'story':         story,
        'author_stories': author_stories,
        'next_story':    next_story,
        'view_count':    story.views.count(),
    })


@login_required
def delete_story(request, pk):
    story = get_object_or_404(Story, pk=pk, author=request.user)
    if request.method == 'POST':
        story.delete()
        messages.success(request, 'Story deleted.')
    return redirect('feed')


@login_required
def my_stories(request):
    """Apni saari active stories"""
    cutoff = timezone.now() - timedelta(hours=24)
    stories = Story.objects.filter(
        author=request.user,
        created_at__gte=cutoff
    ).order_by('-created_at')
    return render(request, 'stories/my_stories.html', {'stories': stories})


# ═══════════════════════════════════════════════
# DIRECT MESSAGES
# ═══════════════════════════════════════════════

@login_required
def dm_inbox(request):
    """Saari conversations list"""
    # Jinse baat hui hai unka unique list
    sent_to = DirectMessage.objects.filter(
        sender=request.user).values_list('receiver_id', flat=True).distinct()
    recv_from = DirectMessage.objects.filter(
        receiver=request.user).values_list('sender_id', flat=True).distinct()
    convo_ids = set(list(sent_to) + list(recv_from))
    convo_users = User.objects.filter(
        id__in=convo_ids).select_related('profile')

    conversations = []
    for u in convo_users:
        last_msg = DirectMessage.objects.filter(
            Q(sender=request.user, receiver=u) |
            Q(sender=u, receiver=request.user)
        ).order_by('-created_at').first()
        unread = DirectMessage.objects.filter(
            sender=u, receiver=request.user, is_read=False).count()
        conversations.append({
            'user':     u,
            'last_msg': last_msg,
            'unread':   unread,
        })
    # Latest conversation upar
    conversations.sort(
        key=lambda x: x['last_msg'].created_at if x['last_msg'] else timezone.now(),
        reverse=True
    )
    return render(request, 'dm/inbox.html', {'conversations': conversations})


@login_required
def dm_conversation(request, username):
    """Ek user ke saath conversation"""
    other = get_object_or_404(User, username=username)
    msgs  = DirectMessage.objects.filter(
        Q(sender=request.user, receiver=other) |
        Q(sender=other, receiver=request.user)
    ).order_by('created_at')

    # Read mark karo
    DirectMessage.objects.filter(
        sender=other, receiver=request.user, is_read=False
    ).update(is_read=True)

    if request.method == 'POST':
        text = request.POST.get('message', '').strip()
        if text:
            DirectMessage.objects.create(
                sender=request.user, receiver=other, message=text)
            return redirect('dm_conversation', username=username)

    return render(request, 'dm/conversation.html', {
        'other': other,
        'msgs':  msgs,
    })


@login_required
def dm_new(request):
    """New DM — following users list"""
    following = User.objects.filter(
        follower_set__follower=request.user
    ).select_related('profile')
    return render(request, 'dm/new_message.html', {'following': following})


# ═══════════════════════════════════════════════
# SHARE POST
# ═══════════════════════════════════════════════

@login_required
def share_post(request, pk):
    """Post ka share URL return karo (AJAX)"""
    post = get_object_or_404(Post, pk=pk)
    post_url = request.build_absolute_uri(f'/posts/{pk}/')
    return JsonResponse({'url': post_url, 'caption': post.caption[:80]})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import SignupForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile, Follow
from posts.models import Post, Notification


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to PixGram, @{user.username}!')
            return redirect('feed')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, @{user.username}!')
            return redirect(request.GET.get('next', 'feed'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('landing')


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts        = profile_user.post_set.all().order_by('-created_at')
    is_following = Follow.objects.filter(
        follower=request.user, following=profile_user
    ).exists()
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'posts':        posts,
        'post_count':   posts.count(),
        'is_following': is_following,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Please fix the errors.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {
        'u_form': u_form, 'p_form': p_form,
    })


@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, "Aap apne aap ko follow nahi kar sakte!")
        return redirect('profile', username=username)

    follow_obj, created = Follow.objects.get_or_create(
        follower=request.user, following=target
    )
    if not created:
        follow_obj.delete()
        messages.info(request, f'@{target.username} ko unfollow kar diya.')
    else:
        messages.success(request, f'@{target.username} ko follow kar liya!')
        # Follow notification bhejo
        Notification.objects.get_or_create(
            recipient  = target,
            sender     = request.user,
            notif_type = 'follow',
            post       = None,
        )
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def followers_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers    = User.objects.filter(
        following_set__following=profile_user
    ).select_related('profile')
    my_following = set(
        Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    )
    return render(request, 'accounts/follow_list.html', {
        'profile_user': profile_user,
        'people':       followers,
        'my_following': my_following,
        'title':        'Followers',
    })


@login_required
def following_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    following    = User.objects.filter(
        follower_set__follower=profile_user
    ).select_related('profile')
    my_following = set(
        Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    )
    return render(request, 'accounts/follow_list.html', {
        'profile_user': profile_user,
        'people':       following,
        'my_following': my_following,
        'title':        'Following',
    })


@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    users = []
    posts = []
    my_following = set()

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id).select_related('profile')[:15]

        posts = Post.objects.filter(
            Q(caption__icontains=query)
        ).select_related('author', 'author__profile')[:12]

        my_following = set(
            Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
        )

    return render(request, 'accounts/search.html', {
        'query': query, 'users': users,
        'posts': posts, 'my_following': my_following,
    })
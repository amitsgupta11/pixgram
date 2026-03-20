from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Post(models.Model):
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    caption    = models.TextField(max_length=2200)
    image      = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username}: {self.caption[:40]}'

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()


class Like(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text       = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class SavedPost(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering        = ['-created_at']


class Notification(models.Model):
    TYPES = [
        ('like',    'liked your post'),
        ('comment', 'commented on your post'),
        ('follow',  'started following you'),
    ]
    recipient  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notif_type = models.CharField(max_length=20, choices=TYPES)
    post       = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


# ─── Stories ───────────────────────────────────────────────
class Story(models.Model):
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image      = models.ImageField(upload_to='stories/')
    caption    = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_active(self):
        """24 ghante ke andar hai?"""
        return timezone.now() < self.created_at + timedelta(hours=24)

    @property
    def time_left(self):
        """Kitna time bacha hai expire hone mein"""
        expires = self.created_at + timedelta(hours=24)
        remaining = expires - timezone.now()
        hours = int(remaining.total_seconds() // 3600)
        return f'{hours}h left'

    def __str__(self):
        return f'{self.author.username} story – {self.created_at}'


class StoryView(models.Model):
    """Kisne story dekhi"""
    story      = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    viewer     = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'viewer')


# ─── Direct Messages ───────────────────────────────────────
class DirectMessage(models.Model):
    sender     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_dms')
    receiver   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_dms')
    message    = models.TextField(max_length=1000)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username} → {self.receiver.username}: {self.message[:30]}'
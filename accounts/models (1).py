from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True)
    bio    = models.TextField(max_length=300, blank=True, default='')

    def __str__(self):
        return f'{self.user.username} – Profile'

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return f'https://ui-avatars.com/api/?name={self.user.username}&background=random&color=fff&size=128'

    # ── Follow counts ──
    @property
    def follower_count(self):
        return Follow.objects.filter(following=self.user).count()

    @property
    def following_count(self):
        return Follow.objects.filter(follower=self.user).count()


class Follow(models.Model):
    """
    follower  → jo follow kar raha hai
    following → jise follow kiya ja raha hai
    """
    follower   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # ek baar hi follow ho sakta hai

    def __str__(self):
        return f'{self.follower.username} → {self.following.username}'


# ── Signals ──
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

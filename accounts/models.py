from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

class FriendRequest(models.Model):
    from_user = models.ForeignKey('CustomUser', related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey('CustomUser', related_name='received_requests', on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    NOTIF_TYPE_CHOICES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('friend', 'FriendRequest'),
    ]
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE_CHOICES)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.

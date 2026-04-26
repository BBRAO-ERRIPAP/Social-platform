from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    TYPE_CHOICES = [
        ('like',           '❤️ liked your post'),
        ('comment',        '💬 commented on your post'),
        ('follow',         '👤 started following you'),
        ('friend_request', '🤝 sent you a friend request'),
        ('friend_accept',  '✅ accepted your friend request'),
    ]
    recipient         = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications'
    )
    sender            = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications'
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    post              = models.ForeignKey(
        'posts.Post', on_delete=models.CASCADE, null=True, blank=True
    )
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender.username} → {self.recipient.username} [{self.notification_type}]'
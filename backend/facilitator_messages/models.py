from django.db import models
from django.utils import timezone
from circles.models import Circle
from authentication.models import AccessKey


class Message(models.Model):
    """Facilitator messages sent to circles"""
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Plain Text'),
        ('html', 'HTML'),
        ('system', 'System Message'),
    ]
    
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='messages')
    sender_key = models.ForeignKey(
        AccessKey, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'facilitator'}
    )
    content = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    is_visible = models.BooleanField(default=True)
    sent_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Message to {self.circle.name}: {self.content[:50]}..."
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-sent_at']

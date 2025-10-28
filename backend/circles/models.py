from django.db import models
from django.utils import timezone
from authentication.models import AccessKey


class Circle(models.Model):
    """Virtual meeting spaces for inquiry groups"""
    STATUS_CHOICES = [
        ('inactive', 'Inactive'),
        ('active', 'Active'),
        ('ended', 'Ended'),
    ]

    CIRCLE_TYPE_CHOICES = [
        ('discussion', 'Discussion'),
        ('translation', 'Translation'),
        ('study', 'Study'),
    ]

    circle_type = models.CharField(
        max_length=20,
        choices=CIRCLE_TYPE_CHOICES,
        default='discussion'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    facilitator_key = models.ForeignKey(
        AccessKey, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'facilitator'}
    )
    jitsi_room_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Circle"
        verbose_name_plural = "Circles"


class CircleParticipant(models.Model):
    """Track participants in circles"""
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='participants')
    access_key = models.ForeignKey(AccessKey, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    is_connected = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.access_key.key} in {self.circle.name}"
    
    class Meta:
        unique_together = ['circle', 'access_key']
        verbose_name = "Circle Participant"
        verbose_name_plural = "Circle Participants"

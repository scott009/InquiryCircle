from django.db import models
from django.utils import timezone


class AccessKey(models.Model):
    """Key-based authentication model for facilitators and participants"""
    ROLE_CHOICES = [
        ('facilitator', 'Facilitator'),
        ('participant', 'Participant'),
    ]
    
    key = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.key} ({self.role})"
    
    class Meta:
        verbose_name = "Access Key"
        verbose_name_plural = "Access Keys"

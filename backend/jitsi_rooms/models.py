from django.db import models
from django.utils import timezone
from circles.models import Circle
import secrets
import string


class JitsiRoom(models.Model):
    """Model for managing Jitsi video conference rooms"""
    
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('active', 'Active'),
        ('ended', 'Ended'),
        ('expired', 'Expired'),
    ]
    
    # Room identification
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='jitsi_rooms')
    room_name = models.CharField(max_length=255, unique=True)
    room_password = models.CharField(max_length=50, blank=True)
    
    # Room configuration
    moderator_name = models.CharField(max_length=100, default='Facilitator')
    max_participants = models.IntegerField(default=20)
    enable_lobby = models.BooleanField(default=True)
    enable_recording = models.BooleanField(default=False)
    
    # Room lifecycle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Tracking
    participant_count = models.IntegerField(default=0)
    last_activity = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['circle', 'status']),
            models.Index(fields=['room_name']),
        ]
    
    def __str__(self):
        return f"Room {self.room_name} for {self.circle.name}"
    
    @classmethod
    def generate_room_name(cls, circle_id: str) -> str:
        """Generate a secure room name"""
        # Create a short random suffix
        random_suffix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        timestamp_suffix = str(timezone.now().timestamp()).split('.')[-1][:4]
        return f"ic-{circle_id}-{random_suffix}-{timestamp_suffix}"
    
    @classmethod
    def generate_room_password(cls) -> str:
        """Generate a secure room password"""
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    
    def start_room(self):
        """Mark room as active"""
        if self.status == 'created':
            self.status = 'active'
            self.started_at = timezone.now()
            self.save(update_fields=['status', 'started_at'])
    
    def end_room(self):
        """Mark room as ended"""
        if self.status == 'active':
            self.status = 'ended'
            self.ended_at = timezone.now()
            self.save(update_fields=['status', 'ended_at'])
    
    def update_activity(self, participant_count: int = None):
        """Update room activity and participant count"""
        self.last_activity = timezone.now()
        if participant_count is not None:
            self.participant_count = participant_count
        self.save(update_fields=['last_activity', 'participant_count'])
    
    def is_expired(self) -> bool:
        """Check if room has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def get_join_config(self, user_role: str = 'participant') -> dict:
        """Get Jitsi configuration for joining this room"""
        return {
            'roomName': self.room_name,
            'password': self.room_password if self.room_password else None,
            'moderator': user_role == 'facilitator',
            'subject': f"{self.circle.name} - InquiryCircle Session",
            'maxParticipants': self.max_participants,
            'enableLobby': self.enable_lobby,
            'enableRecording': self.enable_recording
        }


class RoomParticipant(models.Model):
    """Track participants in Jitsi rooms"""
    
    room = models.ForeignKey(JitsiRoom, on_delete=models.CASCADE, related_name='participants')
    participant_id = models.CharField(max_length=255)  # Jitsi participant ID
    display_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=[('moderator', 'Moderator'), ('participant', 'Participant')])
    
    joined_at = models.DateTimeField(default=timezone.now)
    left_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Activity tracking
    speak_time = models.DurationField(default=timezone.timedelta)  # Total time speaking
    last_activity = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['room', 'participant_id']
        ordering = ['joined_at']
    
    def __str__(self):
        return f"{self.display_name} in {self.room.room_name}"
    
    def leave_room(self):
        """Mark participant as left"""
        self.is_active = False
        self.left_at = timezone.now()
        self.save(update_fields=['is_active', 'left_at'])
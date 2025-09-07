from django.contrib import admin
from .models import JitsiRoom, RoomParticipant


@admin.register(JitsiRoom)
class JitsiRoomAdmin(admin.ModelAdmin):
    list_display = [
        'room_name', 'circle', 'status', 'participant_count', 
        'created_at', 'started_at', 'ended_at'
    ]
    list_filter = ['status', 'enable_lobby', 'enable_recording', 'created_at']
    search_fields = ['room_name', 'circle__name']
    readonly_fields = ['room_name', 'created_at', 'started_at', 'ended_at', 'last_activity']
    
    fieldsets = (
        ('Room Information', {
            'fields': ('circle', 'room_name', 'room_password', 'status')
        }),
        ('Configuration', {
            'fields': ('moderator_name', 'max_participants', 'enable_lobby', 'enable_recording')
        }),
        ('Lifecycle', {
            'fields': ('created_at', 'started_at', 'ended_at', 'expires_at')
        }),
        ('Activity', {
            'fields': ('participant_count', 'last_activity')
        })
    )
    
    def has_delete_permission(self, request, obj=None):
        # Only allow deletion of ended rooms
        if obj and obj.status in ['active', 'created']:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(RoomParticipant)
class RoomParticipantAdmin(admin.ModelAdmin):
    list_display = [
        'display_name', 'room', 'role', 'is_active', 
        'joined_at', 'left_at'
    ]
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['display_name', 'room__room_name', 'participant_id']
    readonly_fields = ['participant_id', 'joined_at', 'left_at', 'last_activity']
    
    fieldsets = (
        ('Participant Info', {
            'fields': ('room', 'participant_id', 'display_name', 'role')
        }),
        ('Activity', {
            'fields': ('joined_at', 'left_at', 'is_active', 'last_activity')
        }),
        ('Statistics', {
            'fields': ('speak_time',)
        })
    )
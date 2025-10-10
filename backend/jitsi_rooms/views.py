from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
from authentication.views import get_key_from_request
from circles.models import Circle
from .models import JitsiRoom, RoomParticipant
import json


@api_view(['POST'])
def create_room(request):
    """Create a new Jitsi room for a circle"""
    access_key, error_msg = get_key_from_request(request)
    if not access_key:
        return JsonResponse({'error': error_msg}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Only facilitators can create rooms
    if access_key.role != 'facilitator':
        return JsonResponse({'error': 'Only facilitators can create rooms'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        data = json.loads(request.body)
        circle_id = data.get('circle_id')
        
        if not circle_id:
            return JsonResponse({'error': 'circle_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the circle
        try:
            circle = Circle.objects.get(id=circle_id)
        except Circle.DoesNotExist:
            return JsonResponse({'error': 'Circle not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if there's already an active room for this circle
        existing_room = JitsiRoom.objects.filter(
            circle=circle, 
            status__in=['created', 'active']
        ).first()
        
        if existing_room:
            return JsonResponse({
                'room_id': existing_room.id,
                'room_name': existing_room.room_name,
                'room_password': existing_room.room_password,
                'status': existing_room.status,
                'config': existing_room.get_join_config('facilitator'),
                'message': 'Using existing active room'
            })
        
        # Create new room
        room = JitsiRoom.objects.create(
            circle=circle,
            room_name=JitsiRoom.generate_room_name(str(circle_id)),
            room_password=JitsiRoom.generate_room_password(),
            moderator_name=f'Facilitator',
            enable_lobby=data.get('enable_lobby', True),
            enable_recording=data.get('enable_recording', False),
            max_participants=data.get('max_participants', 20),
            expires_at=timezone.now() + timezone.timedelta(hours=4)  # 4 hour sessions
        )
        
        return JsonResponse({
            'room_id': room.id,
            'room_name': room.room_name,
            'room_password': room.room_password,
            'status': room.status,
            'config': room.get_join_config('facilitator'),
            'created_at': room.created_at.isoformat()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_room_config(request, circle_id):
    """Get room configuration for joining a circle's video conference"""
    access_key, error_msg = get_key_from_request(request)
    if not access_key:
        return JsonResponse({'error': error_msg}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Get the circle
        try:
            circle = Circle.objects.get(id=circle_id)
        except Circle.DoesNotExist:
            return JsonResponse({'error': 'Circle not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get active room for this circle
        room = JitsiRoom.objects.filter(
            circle=circle,
            status__in=['created', 'active']
        ).first()
        
        if not room:
            return JsonResponse({'error': 'No active room found for this circle'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if room has expired
        if room.is_expired():
            room.status = 'expired'
            room.save()
            return JsonResponse({'error': 'Room has expired'}, status=status.HTTP_410_GONE)
        
        return JsonResponse({
            'room_id': room.id,
            'room_name': room.room_name,
            'room_password': room.room_password,
            'status': room.status,
            'config': room.get_join_config(access_key.role),
            'participant_count': room.participant_count,
            'max_participants': room.max_participants,
            'created_at': room.created_at.isoformat(),
            'expires_at': room.expires_at.isoformat() if room.expires_at else None
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def join_room(request, room_id):
    """Record participant joining a room"""
    access_key, error_msg = get_key_from_request(request)
    if not access_key:
        return JsonResponse({'error': error_msg}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        data = json.loads(request.body)
        participant_id = data.get('participant_id')
        display_name = data.get('display_name', 'Anonymous')
        
        if not participant_id:
            return JsonResponse({'error': 'participant_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the room
        try:
            room = JitsiRoom.objects.get(id=room_id)
        except JitsiRoom.DoesNotExist:
            return JsonResponse({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Start the room if it's just created
        if room.status == 'created':
            room.start_room()
        
        # Create or update participant
        participant, created = RoomParticipant.objects.get_or_create(
            room=room,
            participant_id=participant_id,
            defaults={
                'display_name': display_name,
                'role': 'moderator' if access_key.role == 'facilitator' else 'participant',
                'is_active': True
            }
        )
        
        if not created and not participant.is_active:
            # Participant rejoining
            participant.is_active = True
            participant.joined_at = timezone.now()
            participant.left_at = None
            participant.save()
        
        # Update room activity
        active_participants = RoomParticipant.objects.filter(room=room, is_active=True).count()
        room.update_activity(active_participants)
        
        return JsonResponse({
            'success': True,
            'participant_id': participant.participant_id,
            'role': participant.role,
            'room_status': room.status,
            'active_participants': active_participants
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def leave_room(request, room_id):
    """Record participant leaving a room"""
    access_key, error_msg = get_key_from_request(request)
    if not access_key:
        return JsonResponse({'error': error_msg}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        data = json.loads(request.body)
        participant_id = data.get('participant_id')
        
        if not participant_id:
            return JsonResponse({'error': 'participant_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the room
        try:
            room = JitsiRoom.objects.get(id=room_id)
        except JitsiRoom.DoesNotExist:
            return JsonResponse({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Find and update participant
        try:
            participant = RoomParticipant.objects.get(room=room, participant_id=participant_id)
            participant.leave_room()
        except RoomParticipant.DoesNotExist:
            # Participant wasn't recorded as joined, that's OK
            pass
        
        # Update room activity
        active_participants = RoomParticipant.objects.filter(room=room, is_active=True).count()
        room.update_activity(active_participants)
        
        # End room if no active participants and it's been active for a while
        if active_participants == 0 and room.status == 'active':
            time_since_start = timezone.now() - (room.started_at or room.created_at)
            if time_since_start.total_seconds() > 300:  # 5 minutes minimum session
                room.end_room()
        
        return JsonResponse({
            'success': True,
            'room_status': room.status,
            'active_participants': active_participants
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def room_stats(request, room_id):
    """Get room statistics"""
    access_key, error_msg = get_key_from_request(request)
    if not access_key:
        return JsonResponse({'error': error_msg}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Get the room
        try:
            room = JitsiRoom.objects.get(id=room_id)
        except JitsiRoom.DoesNotExist:
            return JsonResponse({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Only facilitators can see detailed stats
        if access_key.role != 'facilitator':
            return JsonResponse({'error': 'Only facilitators can view room statistics'}, status=status.HTTP_403_FORBIDDEN)
        
        participants = RoomParticipant.objects.filter(room=room)
        active_participants = participants.filter(is_active=True)
        
        return JsonResponse({
            'room_id': room.id,
            'room_name': room.room_name,
            'status': room.status,
            'created_at': room.created_at.isoformat(),
            'started_at': room.started_at.isoformat() if room.started_at else None,
            'ended_at': room.ended_at.isoformat() if room.ended_at else None,
            'total_participants': participants.count(),
            'active_participants': active_participants.count(),
            'max_concurrent': room.participant_count,
            'participants': [
                {
                    'id': p.participant_id,
                    'display_name': p.display_name,
                    'role': p.role,
                    'joined_at': p.joined_at.isoformat(),
                    'left_at': p.left_at.isoformat() if p.left_at else None,
                    'is_active': p.is_active
                }
                for p in participants
            ]
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def jitsi_config(request):
    """Return JaaS configuration for frontend"""
    return JsonResponse({
        'domain': settings.JITSI_CONFIG['domain'],
        'app_id': settings.JITSI_CONFIG['app_id'],
        'external_api_url': settings.JITSI_CONFIG['external_api_url'],
        'jwt_enabled': settings.JITSI_CONFIG['jwt_enabled']
    })

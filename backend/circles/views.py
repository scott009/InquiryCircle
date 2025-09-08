import json
import uuid
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from authentication.views import get_key_from_request
from authentication.models import AccessKey
from .models import Circle, CircleParticipant


@api_view(['GET', 'POST'])
def circles_list_create(request):
    """List circles or create new circle"""
    
    # Verify authentication
    access_key, error = get_key_from_request(request)
    if not access_key:
        return JsonResponse({'error': error}, status=401)
    
    if request.method == 'GET':
        if access_key.role == 'facilitator':
            # Facilitators see their own circles
            circles = Circle.objects.filter(facilitator_key=access_key)
        else:
            # Participants see circles they're in
            participant_circles = CircleParticipant.objects.filter(access_key=access_key)
            circles = Circle.objects.filter(id__in=[cp.circle.id for cp in participant_circles])
        
        return JsonResponse({
            'circles': [{
                'id': circle.id,
                'name': circle.name,
                'description': circle.description,
                'status': circle.status,
                'created_at': circle.created_at.isoformat(),
                'jitsi_room_id': circle.jitsi_room_id
            } for circle in circles]
        })
    
    elif request.method == 'POST':
        # Only facilitators can create circles
        if access_key.role != 'facilitator':
            return JsonResponse({'error': 'Only facilitators can create circles'}, status=403)
        
        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description', '')
            
            if not name:
                return JsonResponse({'error': 'Circle name is required'}, status=400)
            
            # Generate unique Jitsi room ID
            jitsi_room_id = f"ic-{uuid.uuid4().hex[:8]}"
            
            circle = Circle.objects.create(
                name=name,
                description=description,
                facilitator_key=access_key,
                jitsi_room_id=jitsi_room_id
            )
            
            return JsonResponse({
                'id': circle.id,
                'name': circle.name,
                'description': circle.description,
                'status': circle.status,
                'created_at': circle.created_at.isoformat(),
                'jitsi_room_id': circle.jitsi_room_id
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET', 'PUT', 'DELETE'])
def circle_detail(request, circle_id):
    """Get, update, or delete a specific circle"""
    
    # Verify authentication
    access_key, error = get_key_from_request(request)
    if not access_key:
        return JsonResponse({'error': error}, status=401)
    
    try:
        circle = Circle.objects.get(id=circle_id)
    except Circle.DoesNotExist:
        return JsonResponse({'error': 'Circle not found'}, status=404)
    
    # Only facilitators can modify their own circles
    if circle.facilitator_key != access_key and access_key.role != 'facilitator':
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'GET':
        # Get circle details with participants
        participants = CircleParticipant.objects.filter(circle=circle)
        participant_keys = AccessKey.objects.filter(id__in=[p.access_key_id for p in participants])
        
        return JsonResponse({
            'id': circle.id,
            'name': circle.name,
            'description': circle.description,
            'status': circle.status,
            'created_at': circle.created_at.isoformat(),
            'jitsi_room_id': circle.jitsi_room_id,
            'participants': [{
                'key_id': key.id,
                'access_key': key.key,
                'role': key.role,
                'created_at': key.created_at.isoformat()
            } for key in participant_keys]
        })
    
    elif request.method == 'PUT':
        # Update circle
        try:
            data = json.loads(request.body)
            if 'name' in data:
                circle.name = data['name']
            if 'description' in data:
                circle.description = data['description']
            if 'status' in data and data['status'] in ['active', 'paused', 'completed']:
                circle.status = data['status']
            
            circle.save()
            
            return JsonResponse({
                'id': circle.id,
                'name': circle.name,
                'description': circle.description,
                'status': circle.status,
                'created_at': circle.created_at.isoformat(),
                'jitsi_room_id': circle.jitsi_room_id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        # Delete circle and all related data
        circle_name = circle.name
        circle.delete()
        return JsonResponse({
            'message': f'Circle "{circle_name}" has been deleted successfully'
        })


@api_view(['POST'])
def generate_participant_key(request, circle_id):
    """Generate a new participant access key for a circle"""
    
    # Verify authentication
    access_key, error = get_key_from_request(request)
    if not access_key or access_key.role != 'facilitator':
        return JsonResponse({'error': 'Only facilitators can generate participant keys'}, status=403)
    
    try:
        circle = Circle.objects.get(id=circle_id)
    except Circle.DoesNotExist:
        return JsonResponse({'error': 'Circle not found'}, status=404)
    
    # Only the circle's facilitator can generate keys
    if circle.facilitator_key != access_key:
        return JsonResponse({'error': 'Only the circle facilitator can generate keys'}, status=403)
    
    try:
        data = json.loads(request.body)
        custom_key = data.get('custom_key', '').strip()
        
        # Use custom key if provided, otherwise generate one
        if custom_key:
            # Check if key already exists
            if AccessKey.objects.filter(key=custom_key).exists():
                return JsonResponse({'error': f'Access key "{custom_key}" already exists'}, status=400)
            access_key_value = custom_key
        else:
            access_key_value = f'participant-{uuid.uuid4().hex}'
        
        # Generate new access key
        new_key = AccessKey.objects.create(
            key=access_key_value,
            role='participant'
        )
        
        # Add to circle
        CircleParticipant.objects.create(
            circle=circle,
            access_key=new_key
        )
        
        return JsonResponse({
            'key_id': new_key.id,
            'access_key': new_key.key,
            'role': new_key.role,
            'created_at': new_key.created_at.isoformat()
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['DELETE'])
def remove_participant_key(request, circle_id, key_id):
    """Remove a participant access key from a circle"""
    
    # Verify authentication
    access_key, error = get_key_from_request(request)
    if not access_key or access_key.role != 'facilitator':
        return JsonResponse({'error': 'Only facilitators can remove participant keys'}, status=403)
    
    try:
        circle = Circle.objects.get(id=circle_id)
    except Circle.DoesNotExist:
        return JsonResponse({'error': 'Circle not found'}, status=404)
    
    # Only the circle's facilitator can remove keys
    if circle.facilitator_key != access_key:
        return JsonResponse({'error': 'Only the circle facilitator can remove keys'}, status=403)
    
    try:
        participant = CircleParticipant.objects.get(circle=circle, access_key_id=key_id)
        key_info = participant.access_key
        participant.delete()
        
        # Optionally delete the access key itself if no longer used
        if not CircleParticipant.objects.filter(access_key=key_info).exists():
            key_info.delete()
        
        return JsonResponse({
            'message': f'Participant key removed from circle "{circle.name}"'
        })
        
    except CircleParticipant.DoesNotExist:
        return JsonResponse({'error': 'Participant key not found in this circle'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

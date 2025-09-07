import json
import uuid
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from authentication.views import get_key_from_request
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

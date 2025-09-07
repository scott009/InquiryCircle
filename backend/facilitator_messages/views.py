import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from authentication.views import get_key_from_request
from circles.models import Circle
from .models import Message


@api_view(['GET', 'POST'])
def messages_list_create(request):
    """List messages or send new message"""
    
    # Verify authentication
    access_key, error = get_key_from_request(request)
    if not access_key:
        return JsonResponse({'error': error}, status=401)
    
    if request.method == 'GET':
        circle_id = request.GET.get('circle_id')
        
        if not circle_id:
            return JsonResponse({'error': 'circle_id parameter required'}, status=400)
        
        try:
            circle = Circle.objects.get(id=circle_id)
            
            # Check if user has access to this circle
            if access_key.role == 'facilitator':
                if circle.facilitator_key != access_key:
                    return JsonResponse({'error': 'Access denied'}, status=403)
            else:
                # Check if participant is in this circle
                from circles.models import CircleParticipant
                if not CircleParticipant.objects.filter(circle=circle, access_key=access_key).exists():
                    return JsonResponse({'error': 'Access denied'}, status=403)
            
            messages = Message.objects.filter(circle=circle, is_visible=True)
            
            return JsonResponse({
                'messages': [{
                    'id': msg.id,
                    'content': msg.content,
                    'message_type': msg.message_type,
                    'sent_at': msg.sent_at.isoformat()
                } for msg in messages]
            })
            
        except Circle.DoesNotExist:
            return JsonResponse({'error': 'Circle not found'}, status=404)
    
    elif request.method == 'POST':
        # Only facilitators can send messages
        if access_key.role != 'facilitator':
            return JsonResponse({'error': 'Only facilitators can send messages'}, status=403)
        
        try:
            data = json.loads(request.body)
            circle_id = data.get('circle_id')
            content = data.get('content')
            message_type = data.get('message_type', 'text')
            
            if not circle_id or not content:
                return JsonResponse({'error': 'circle_id and content are required'}, status=400)
            
            try:
                circle = Circle.objects.get(id=circle_id, facilitator_key=access_key)
            except Circle.DoesNotExist:
                return JsonResponse({'error': 'Circle not found or access denied'}, status=404)
            
            message = Message.objects.create(
                circle=circle,
                sender_key=access_key,
                content=content,
                message_type=message_type
            )
            
            return JsonResponse({
                'id': message.id,
                'content': message.content,
                'message_type': message.message_type,
                'sent_at': message.sent_at.isoformat()
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

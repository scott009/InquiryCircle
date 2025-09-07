from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from .models import AccessKey


@api_view(['POST'])
def verify_key(request):
    """Verify access key and return role information"""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Key '):
        return JsonResponse({
            'valid': False,
            'error': 'Invalid authorization header format'
        }, status=400)
    
    key_value = auth_header[4:]  # Remove 'Key ' prefix
    
    try:
        access_key = AccessKey.objects.get(key=key_value, is_active=True)
        
        # Update last used timestamp
        access_key.last_used = timezone.now()
        access_key.save()
        
        return JsonResponse({
            'valid': True,
            'role': access_key.role,
            'key_id': access_key.id
        })
    
    except AccessKey.DoesNotExist:
        return JsonResponse({
            'valid': False,
            'error': 'Invalid key'
        }, status=401)


def get_key_from_request(request):
    """Helper function to extract and validate key from request"""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Key '):
        return None, 'Invalid authorization header format'
    
    key_value = auth_header[4:]
    
    try:
        access_key = AccessKey.objects.get(key=key_value, is_active=True)
        access_key.last_used = timezone.now()
        access_key.save()
        return access_key, None
    except AccessKey.DoesNotExist:
        return None, 'Invalid key'

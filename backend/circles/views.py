"""
Views for InquiryCircle circles app.
"""
import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import logging
from .storage import storage

logger = logging.getLogger(__name__)

def homepage(request):
    """Homepage with key entry form."""
    return render(request, 'circles/homepage.html')

@csrf_exempt
def validate_key(request):
    """Validate key and route to appropriate view."""
    if request.method == 'POST':
        data = json.loads(request.body)
        key = data.get('key', '').strip()
        
        keys = storage.load_keys()
        circles = storage.load_circles()
        
        if key in keys:
            key_data = keys[key]
            key_type = key_data['type']
            
            if key_type == 'admin':
                return JsonResponse({
                    'valid': True,
                    'redirect': '/admin-dashboard/',
                    'type': 'admin',
                    'name': key_data['name']
                })
            elif key_type in ['facilitator', 'participant']:
                circle_id = key_data['circle_id']
                if circle_id in circles and circles[circle_id]['active']:
                    return JsonResponse({
                        'valid': True,
                        'redirect': f'/circle/{circle_id}/',
                        'type': key_type,
                        'name': key_data['name'],
                        'circle_id': circle_id
                    })
                else:
                    return JsonResponse({'valid': False, 'error': 'Circle not found or inactive'})
        
        return JsonResponse({'valid': False, 'error': 'Invalid key'})
    
    return JsonResponse({'error': 'POST required'}, status=405)

def circle_view(request, circle_id):
    """Display a circle with embedded Jitsi."""
    # Get key from session or query param for validation
    key = request.GET.get('key') or request.session.get('key')
    
    keys = storage.load_keys()
    circles = storage.load_circles()
    
    if not key or key not in keys:
        return redirect('/')
    
    key_data = keys[key]
    
    # Verify key has access to this circle
    if key_data['type'] == 'admin':
        # Admin can access any circle
        pass
    elif key_data.get('circle_id') != circle_id:
        return HttpResponseForbidden("Access denied to this circle")
    
    if circle_id not in circles:
        return render(request, 'circles/error.html', {'error': 'Circle not found'})
    
    circle = circles[circle_id]
    if not circle['active']:
        return render(request, 'circles/error.html', {'error': 'Circle is inactive'})
    
    # Store key in session
    request.session['key'] = key
    
    context = {
        'circle': circle,
        'user_role': key_data['type'],
        'user_name': key_data['name'],
        'jitsi_domain': settings.JITSI_DOMAIN,
        'jitsi_room': circle['jitsi_room'],
        'is_facilitator': key_data['type'] in ['facilitator', 'admin'],
    }
    
    return render(request, 'circles/circle.html', context)

def admin_dashboard(request):
    """Admin dashboard for managing circles and keys."""
    key = request.GET.get('key') or request.session.get('key')
    
    keys = storage.load_keys()
    
    if not key or key not in keys or keys[key]['type'] != 'admin':
        return redirect('/')
    
    request.session['key'] = key
    
    circles = storage.load_circles()
    
    context = {
        'circles': circles,
        'keys': keys,
        'admin_name': keys[key]['name']
    }
    
    return render(request, 'circles/admin_dashboard.html', context)

@csrf_exempt
def admin_api(request):
    """API endpoints for admin operations."""
    key = request.session.get('key')
    
    keys = storage.load_keys()
    
    if not key or key not in keys or keys[key]['type'] != 'admin':
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'create_circle':
            circle_id = data.get('circle_id', '').strip()
            circle_name = data.get('circle_name', '').strip()
            
            if not circle_id or not circle_name:
                return JsonResponse({'error': 'Circle ID and name required'})
            
            circles = storage.load_circles()
            
            if circle_id in circles:
                return JsonResponse({'error': 'Circle ID already exists'})
            
            circles[circle_id] = {
                'id': circle_id,
                'name': circle_name,
                'jitsi_room': f"{settings.JITSI_ROOM_PREFIX}{circle_id}",
                'created_by': key,
                'active': True
            }
            
            storage.save_circles(circles)
            logger.info(f"Admin {key} created circle: {circle_id}")
            
            return JsonResponse({'success': True, 'circle': circles[circle_id]})
        
        elif action == 'create_key':
            new_key = data.get('key', '').strip()
            key_type = data.get('type')
            key_name = data.get('name', '').strip()
            circle_id = data.get('circle_id', '').strip()
            
            if not new_key or not key_type or not key_name:
                return JsonResponse({'error': 'Key, type, and name required'})
            
            keys = storage.load_keys()
            
            if new_key in keys:
                return JsonResponse({'error': 'Key already exists'})
            
            key_data = {'type': key_type, 'name': key_name}
            
            if key_type in ['facilitator', 'participant']:
                circles = storage.load_circles()
                if not circle_id or circle_id not in circles:
                    return JsonResponse({'error': 'Valid circle ID required for facilitator/participant keys'})
                key_data['circle_id'] = circle_id
            
            keys[new_key] = key_data
            storage.save_keys(keys)
            logger.info(f"Admin {key} created key: {new_key} ({key_type})")
            
            return JsonResponse({'success': True, 'key_data': key_data})
        
        elif action == 'toggle_circle':
            circle_id = data.get('circle_id')
            circles = storage.load_circles()
            
            if circle_id in circles:
                circles[circle_id]['active'] = not circles[circle_id]['active']
                storage.save_circles(circles)
                logger.info(f"Admin {key} toggled circle {circle_id}: {circles[circle_id]['active']}")
                return JsonResponse({'success': True, 'active': circles[circle_id]['active']})
            return JsonResponse({'error': 'Circle not found'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

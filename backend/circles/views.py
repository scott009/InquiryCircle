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
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'create_circle':
                circle_id = data.get('circle_id', '').strip()
                circle_name = data.get('circle_name', '').strip()
                
                if not circle_id or not circle_name:
                    return JsonResponse({'success': False, 'error': 'Circle ID and name are required'})
                
                circles = storage.load_circles()
                if circle_id in circles:
                    return JsonResponse({'success': False, 'error': 'Circle ID already exists'})
                
                new_circle = {
                    'id': circle_id,
                    'name': circle_name,
                    'jitsi_room': f"{settings.JITSI_ROOM_PREFIX}{circle_id}",
                    'created_by': 'admin',
                    'active': True,
                    'message': ''  # Initialize with empty message
                }
                
                circles[circle_id] = new_circle
                storage.save_circles(circles)
                logger.info(f"Created new circle: {circle_id}")
                
                return JsonResponse({'success': True, 'circle': new_circle})
            
            elif action == 'create_key':
                key_id = data.get('key_id', '').strip()
                key_type = data.get('key_type', '').strip()
                key_name = data.get('key_name', '').strip()
                circle_id = data.get('circle_id', '').strip() if key_type in ['facilitator', 'participant'] else None
                
                if not key_id or not key_type or not key_name:
                    return JsonResponse({'success': False, 'error': 'Key ID, type, and name are required'})
                
                keys = storage.load_keys()
                if key_id in keys:
                    return JsonResponse({'success': False, 'error': 'Key ID already exists'})
                
                new_key = {
                    'type': key_type,
                    'name': key_name
                }
                
                if circle_id:
                    circles = storage.load_circles()
                    if circle_id not in circles:
                        return JsonResponse({'success': False, 'error': 'Circle does not exist'})
                    new_key['circle_id'] = circle_id
                
                keys[key_id] = new_key
                storage.save_keys(keys)
                logger.info(f"Created new key: {key_id}")
                
                return JsonResponse({'success': True, 'key': new_key})
            
            elif action == 'toggle_circle':
                circle_id = data.get('circle_id', '').strip()
                
                circles = storage.load_circles()
                if circle_id not in circles:
                    return JsonResponse({'success': False, 'error': 'Circle not found'})
                
                circles[circle_id]['active'] = not circles[circle_id]['active']
                storage.save_circles(circles)
                logger.info(f"Toggled circle {circle_id} to {'active' if circles[circle_id]['active'] else 'inactive'}")
                
                return JsonResponse({'success': True, 'active': circles[circle_id]['active']})
            
            elif action == 'update_message':
                circle_id = data.get('circle_id', '').strip()
                message = data.get('message', '').strip()
                
                if not circle_id:
                    return JsonResponse({'success': False, 'error': 'Circle ID is required'})
                
                success = storage.update_circle_message(circle_id, message)
                if success:
                    return JsonResponse({'success': True, 'message': 'Message updated successfully'})
                else:
                    return JsonResponse({'success': False, 'error': 'Circle not found'})
            
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        except Exception as e:
            logger.error(f"Admin API error: {e}")
            return JsonResponse({'success': False, 'error': 'Server error'})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def facilitator_api(request):
    """API endpoints for facilitator operations."""
    key = request.session.get('key')
    
    keys = storage.load_keys()
    
    if not key or key not in keys:
        return JsonResponse({'error': 'Authentication required'}, status=403)
    
    key_data = keys[key]
    if key_data['type'] not in ['facilitator', 'admin']:
        return JsonResponse({'error': 'Facilitator access required'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'update_message':
                circle_id = data.get('circle_id', '').strip()
                message = data.get('message', '').strip()
                
                if not circle_id:
                    return JsonResponse({'success': False, 'error': 'Circle ID is required'})
                
                # Verify facilitator has access to this circle
                if key_data['type'] == 'facilitator' and key_data.get('circle_id') != circle_id:
                    return JsonResponse({'success': False, 'error': 'Access denied to this circle'})
                
                success = storage.update_circle_message(circle_id, message)
                if success:
                    logger.info(f"Facilitator {key_data['name']} updated message for circle {circle_id}")
                    return JsonResponse({'success': True, 'message': 'Message updated successfully'})
                else:
                    return JsonResponse({'success': False, 'error': 'Circle not found'})
            
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        except Exception as e:
            logger.error(f"Facilitator API error: {e}")
            return JsonResponse({'success': False, 'error': 'Server error'})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

def debug_circle_data(request, circle_id):
    """Debug endpoint to check circle data - REMOVE IN PRODUCTION"""
    circles = storage.load_circles()
    if circle_id in circles:
        circle_data = circles[circle_id]
        return JsonResponse({
            'circle_id': circle_id,
            'circle_data': circle_data,
            'message_length': len(circle_data.get('message', '')),
            'message_content': circle_data.get('message', ''),
        })
    else:
        return JsonResponse({'error': 'Circle not found'}, status=404)

from django.http import JsonResponse
from django.db import connection
from rest_framework.decorators import api_view


@api_view(['GET'])
def health_check(request):
    """Health check endpoint to verify Django and database connectivity"""
    try:
        # Test database connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'database': 'disconnected',
            'error': str(e)
        }, status=500)

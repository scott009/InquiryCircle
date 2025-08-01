"""
URL patterns for circles app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('validate-key/', views.validate_key, name='validate_key'),
    path('circle/<str:circle_id>/', views.circle_view, name='circle_view'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-api/', views.admin_api, name='admin_api'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('verify-key/', views.verify_key, name='verify_key'),
]
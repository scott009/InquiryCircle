from django.urls import path
from . import views

urlpatterns = [
    path('', views.messages_list_create, name='messages_list_create'),
]
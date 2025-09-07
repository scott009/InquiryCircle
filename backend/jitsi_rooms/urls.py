from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_room, name='create_room'),
    path('circle/<int:circle_id>/', views.get_room_config, name='get_room_config'),
    path('<int:room_id>/join/', views.join_room, name='join_room'),
    path('<int:room_id>/leave/', views.leave_room, name='leave_room'),
    path('<int:room_id>/stats/', views.room_stats, name='room_stats'),
]
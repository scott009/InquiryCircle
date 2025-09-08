from django.urls import path
from . import views

urlpatterns = [
    path('', views.circles_list_create, name='circles_list_create'),
    path('<int:circle_id>/', views.circle_detail, name='circle_detail'),
    path('<int:circle_id>/keys/generate/', views.generate_participant_key, name='generate_participant_key'),
    path('<int:circle_id>/keys/<int:key_id>/remove/', views.remove_participant_key, name='remove_participant_key'),
]
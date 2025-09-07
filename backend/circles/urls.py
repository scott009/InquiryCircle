from django.urls import path
from . import views

urlpatterns = [
    path('', views.circles_list_create, name='circles_list_create'),
]
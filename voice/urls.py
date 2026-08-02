from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_voice, name='register_voice'),
    path('get_command/', views.get_command, name='get_command'),
]

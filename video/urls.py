from django.urls import path
from . import views

urlpatterns = [
    path('join/<int:pk>/', views.join_session, name='join_session'),
    path('my/', views.list_sessions, name='list_sessions'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.view_profile, name='view_profile'),
    path('me/edit/', views.edit_profile, name='edit_profile'),
]

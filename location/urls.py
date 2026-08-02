from django.urls import path
from . import views

urlpatterns = [
    path('', views.live_location, name='live_location'),
    path('save/', views.save_point, name='save_point'),
]

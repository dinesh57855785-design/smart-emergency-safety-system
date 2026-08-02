from django.urls import path
from . import views

urlpatterns = [
    path('update_location/', views.update_location, name='update_location'),
    path('send_initial/', views.send_initial, name='send_initial'),
]

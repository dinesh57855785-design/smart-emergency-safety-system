from django.urls import path
from . import views

urlpatterns = [
    path('', views.sos_page, name='sos_page'),
    path('trigger/', views.trigger_sos, name='trigger_sos'),
]

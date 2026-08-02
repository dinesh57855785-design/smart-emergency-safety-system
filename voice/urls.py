from django.urls import path
from . import views

app_name = "voice"

urlpatterns = [
    path("", views.voice_home, name="home"),
    path("register/", views.voice_register, name="register"),
    path("command/", views.voice_command, name="command"),
]

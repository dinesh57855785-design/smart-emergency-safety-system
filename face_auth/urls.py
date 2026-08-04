from django.urls import path
from . import views

app_name = "face_auth"

urlpatterns = [
    path("register/", views.face_register_api, name="register"),
    path("login/", views.face_login_api, name="login"),
    path("status/", views.face_status_api, name="status"),
]

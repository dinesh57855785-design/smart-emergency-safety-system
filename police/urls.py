from django.urls import path
from . import views

app_name = "police"

urlpatterns = [
    path("notify/", views.notify_page, name="notify"),
]

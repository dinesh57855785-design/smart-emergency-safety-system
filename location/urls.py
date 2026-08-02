from django.urls import path
from . import views

app_name = "location"

urlpatterns = [
    path("", views.location_view, name="view"),
    path("latest/<int:user_id>/", views.latest_location, name="latest"),
    path("update/", views.update_location, name="update"),
]

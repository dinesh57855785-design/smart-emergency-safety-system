from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.profile_view, name="view"),
    path("edit/", views.profile_edit, name="edit"),
    path("review-done/", views.mark_reviewed, name="mark_reviewed"),
]

"""
Main URL configuration for Smart Emergency System.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("profile/", include("profiles.urls")),
    path("contacts/", include("contacts.urls")),
    path("sos/", include("sos.urls")),
    path("location/", include("location.urls")),
    path("video/", include("video.urls")),
    path("voice/", include("voice.urls")),
    path("police/", include("police.urls")),
    path("notifications/", include("notifications.urls")),
    path("reports/", include("reports.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("face-auth/", include("face_auth.urls")),
    path("", RedirectView.as_view(url="/dashboard/", permanent=False)),
]

from django.urls import path
from . import views

app_name = "sos"

urlpatterns = [
    path("", views.sos_page, name="page"),
    path("trigger/", views.trigger_sos, name="trigger"),
    path("update-location/<uuid:event_id>/", views.update_location, name="update_location"),
    path("upload-voice/<uuid:event_id>/", views.upload_voice, name="upload_voice"),
    path("end/<uuid:event_id>/", views.end_sos, name="end_sos"),
    path("history/", views.sos_history, name="history"),
]

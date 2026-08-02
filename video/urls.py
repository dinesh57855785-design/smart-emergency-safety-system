from django.urls import path
from . import views

app_name = "video"

urlpatterns = [
    path("", views.video_list, name="list"),
    path("room/<str:room_name>/", views.video_room, name="room"),
    path("upload-offline/", views.upload_offline, name="upload_offline"),
]

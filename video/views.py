import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import VideoSession, OfflineRecording


@login_required
def video_list(request):
    sessions = VideoSession.objects.filter(user=request.user)
    return render(request, "video/list.html", {
        "sessions": sessions,
        "jitsi_domain": settings.JITSI_DOMAIN,
    })


@login_required
def video_room(request, room_name):
    session = get_object_or_404(VideoSession, room_name=room_name, user=request.user)
    return render(request, "video/room.html", {
        "session": session,
        "jitsi_domain": settings.JITSI_DOMAIN,
    })


@login_required
def upload_offline(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    video_file = request.FILES.get("video")
    if not video_file:
        return HttpResponseBadRequest("No video file received")
    recording = OfflineRecording.objects.create(user=request.user, video_file=video_file, upload_status="uploaded", synced_at=timezone.now())
    return JsonResponse({"ok": True, "recording_id": recording.id})

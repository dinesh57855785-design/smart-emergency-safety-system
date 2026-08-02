import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

from .models import VoiceMessage


EMERGENCY_COMMANDS = {"help", "emergency", "sos", "save me", "call police"}


@login_required
def voice_home(request):
    messages = VoiceMessage.objects.filter(user=request.user)
    return render(request, "voice/voice_listener.html", {"voice_messages": messages})


@login_required
def voice_register(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    audio_file = request.FILES.get("audio")
    transcript = request.POST.get("transcript", "")
    if not audio_file:
        return HttpResponseBadRequest("No audio file received")
    vm = VoiceMessage.objects.create(user=request.user, audio_file=audio_file, transcript=transcript)
    return JsonResponse({"ok": True, "id": str(vm.id), "url": vm.audio_file.url})


@login_required
def voice_command(request):
    """Recognize an emergency voice command and return whether it should trigger SOS."""
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    data = json.loads(request.body or "{}")
    phrase = (data.get("phrase") or "").strip().lower()
    triggered = phrase in EMERGENCY_COMMANDS
    return JsonResponse({"phrase": phrase, "trigger_sos": triggered})

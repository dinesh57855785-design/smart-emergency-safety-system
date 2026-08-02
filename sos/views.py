import json
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from contacts.models import TrustedContact
from .models import SOSEvent, SOSEventContact


def _generate_room_name(user):
    return f"emergency-{user.id}-{int(timezone.now().timestamp())}"


def _build_room_url(room_name):
    return f"https://{settings.JITSI_DOMAIN}/{room_name}"


@login_required
def sos_page(request):
    return render(request, "sos/sos.html", {"google_maps_api_key": settings.GOOGLE_MAPS_API_KEY})


@login_required
def trigger_sos(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    data = json.loads(request.body or "{}")
    lat = data.get("latitude")
    lng = data.get("longitude")
    location_url = ""
    if lat is not None and lng is not None:
        location_url = f"https://www.google.com/maps?q={lat},{lng}"

    room_name = _generate_room_name(request.user)
    room_url = _build_room_url(room_name)

    event = SOSEvent.objects.create(
        user=request.user,
        latitude=lat,
        longitude=lng,
        location_url=location_url,
        video_room_name=room_name,
        video_room_url=room_url,
        video_status="active",
    )

    # Snapshot trusted contacts into the event
    contacts = TrustedContact.objects.filter(user=request.user)[:10]
    contact_records = []
    for c in contacts:
        contact_records.append(SOSEventContact(
            sos_event=event,
            name=c.name,
            relationship=c.relationship,
            mobile_number=c.mobile_number,
        ))
    SOSEventContact.objects.bulk_create(contact_records)

    # Defer to services (imported lazily to avoid circular imports)
    from notifications.services import send_sos_sms_alerts, send_sos_email_alerts
    from police.services import notify_nearest_police

    sms_summary = send_sos_sms_alerts(event)
    send_sos_email_alerts(event)
    police_summary = notify_nearest_police(event)

    event.sms_status = sms_summary
    event.police_status = police_summary
    event.save()

    return JsonResponse({
        "event_id": str(event.id),
        "video_room_url": event.video_room_url,
        "video_room_name": event.video_room_name,
        "sms_status": event.sms_status,
        "police_status": event.police_status,
    })


@login_required
def update_location(request, event_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    event = get_object_or_404(SOSEvent, id=event_id, user=request.user)
    data = json.loads(request.body or "{}")
    lat = data.get("latitude")
    lng = data.get("longitude")
    if lat is not None and lng is not None:
        event.latitude = lat
        event.longitude = lng
        event.location_url = f"https://www.google.com/maps?q={lat},{lng}"
        event.save()
        return JsonResponse({"ok": True, "location_url": event.location_url})
    return HttpResponseBadRequest("Missing coordinates")


@login_required
@csrf_exempt
def upload_voice(request, event_id):
    event = get_object_or_404(SOSEvent, id=event_id, user=request.user)
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    audio_file = request.FILES.get("audio")
    if not audio_file:
        return HttpResponseBadRequest("No audio file received")
    event.voice_message = audio_file
    event.voice_status = "received"
    event.save()
    return JsonResponse({"ok": True, "voice_url": event.voice_message.url})


@login_required
def end_sos(request, event_id):
    event = get_object_or_404(SOSEvent, id=event_id, user=request.user)
    if request.method == "POST":
        event.status = "resolved"
        event.ended_at = timezone.now()
        event.video_status = "ended"
        event.save()
    return redirect("sos:history")


@login_required
def sos_history(request):
    events = SOSEvent.objects.filter(user=request.user)
    return render(request, "sos/history.html", {"events": events})

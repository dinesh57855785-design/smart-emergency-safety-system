import json
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render

from .models import LocationUpdate


@login_required
def location_view(request):
    return render(request, "location/location.html", {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    })


@login_required
def latest_location(request, user_id):
    update = LocationUpdate.objects.filter(user_id=user_id).first()
    if not update:
        return JsonResponse({"available": False})
    return JsonResponse({
        "available": True,
        "latitude": update.latitude,
        "longitude": update.longitude,
        "accuracy": update.accuracy,
        "recorded_at": update.recorded_at.isoformat(),
    })


@login_required
def update_location(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    data = json.loads(request.body or "{}")
    lat = data.get("latitude")
    lng = data.get("longitude")
    acc = data.get("accuracy")
    if lat is None or lng is None:
        return HttpResponseBadRequest("Missing coordinates")
    LocationUpdate.objects.create(user=request.user, latitude=lat, longitude=lng, accuracy=acc)
    return JsonResponse({"ok": True})

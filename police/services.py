"""
Police station detection and notification services.

Primary: Google Places API (Nearby Search) when GOOGLE_MAPS_API_KEY is set.
Fallback: OpenStreetMap Overpass API (no key required).
"""
import math
import requests
from django.conf import settings
from django.utils import timezone

from .models import PoliceStation, PoliceNotification


def _haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def find_nearest_police_station(latitude, longitude):
    """Return the nearest PoliceStation (creating/caching it) or None on failure."""
    if not _is_valid_coord(latitude, longitude):
        return None

    # Try Google Places first
    if settings.GOOGLE_MAPS_API_KEY:
        station = _find_via_google_places(latitude, longitude)
        if station:
            return station

    # Fallback to OpenStreetMap Overpass API
    station = _find_via_openstreetmap(latitude, longitude)
    return station


def _is_valid_coord(lat, lng):
    return lat is not None and lng is not None and -90 <= lat <= 90 and -180 <= lng <= 180


def _find_via_google_places(latitude, longitude):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": 5000,
        "type": "police",
        "key": settings.GOOGLE_MAPS_API_KEY,
    }
    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None

    results = data.get("results", [])
    if not results:
        return None

    # Sort by haversine distance to user
    results.sort(key=lambda r: _haversine_distance(latitude, longitude, r["geometry"]["location"]["lat"], r["geometry"]["location"]["lng"]))
    nearest = results[0]
    loc = nearest["geometry"]["location"]
    place_id = nearest.get("place_id", "")

    station, _ = PoliceStation.objects.update_or_create(
        place_id=place_id or f"g-{loc['lat']}-{loc['lng']}",
        defaults={
            "name": nearest.get("name", "Police Station"),
            "address": nearest.get("vicinity", ""),
            "latitude": loc["lat"],
            "longitude": loc["lng"],
        },
    )
    return station


def _find_via_openstreetmap(latitude, longitude):
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="police"](around:5000,{latitude},{longitude});
      way["amenity"="police"](around:5000,{latitude},{longitude});
    );
    out centers 10;
    """
    try:
        resp = requests.post(overpass_url, data={"data": query}, timeout=12)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None

    elements = data.get("elements", [])
    if not elements:
        return None

    def el_coord(el):
        if "lat" in el:
            return el["lat"], el["lon"]
        if "center" in el:
            return el["center"]["lat"], el["center"]["lon"]
        return None, None

    def el_distance(el):
        lat, lon = el_coord(el)
        return _haversine_distance(latitude, longitude, lat, lon) if lat is not None else float("inf")

    elements.sort(key=el_distance)
    nearest = elements[0]
    lat, lon = el_coord(nearest)
    if lat is None:
        return None
    tags = nearest.get("tags", {})
    name = tags.get("name", "Police Station")
    place_id = f"osm-{nearest.get('id', '')}"

    station, _ = PoliceStation.objects.update_or_create(
        place_id=place_id,
        defaults={
            "name": name,
            "address": tags.get("addr:full", ""),
            "latitude": lat,
            "longitude": lon,
            "phone": tags.get("phone", tags.get("contact:phone", "")),
        },
    )
    return station


def notify_nearest_police(sos_event):
    """Locate nearest station and record a notification. Returns a summary string."""
    station = find_nearest_police_station(sos_event.latitude, sos_event.longitude)
    if not station:
        PoliceNotification.objects.update_or_create(
            sos_event=sos_event,
            defaults={"status": "failed", "error": "No police station found", "station": None},
        )
        sos_event.police_station_name = ""
        sos_event.police_station_address = ""
        sos_event.police_station_phone = ""
        return "failed: no station found"

    message = (
        f"EMERGENCY ALERT from {sos_event.user.email}. "
        f"Location: https://www.google.com/maps?q={sos_event.latitude},{sos_event.longitude}. "
        f"Nearest station: {station.name}. Please respond immediately."
    )
    PoliceNotification.objects.update_or_create(
        sos_event=sos_event,
        defaults={
            "station": station,
            "status": "sent",
            "message": message,
            "sent_at": timezone.now(),
        },
    )
    sos_event.police_station_name = station.name
    sos_event.police_station_address = station.address
    sos_event.police_station_phone = station.phone
    return f"sent: {station.name}"

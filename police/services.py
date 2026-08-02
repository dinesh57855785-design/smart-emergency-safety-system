import os
import json
import requests
from django.conf import settings
from django.utils import timezone
from .models import PoliceStation, PoliceNotification

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

HEADERS = {'User-Agent': 'SmartEmergencySystem/1.0 (+https://github.com/)'}


def _find_nearest_with_google(lat, lon):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lon}',
        'radius': 5000,
        'type': 'police',
        'key': GOOGLE_MAPS_API_KEY,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results = data.get('results', [])
    if not results:
        return None
    first = results[0]
    station = {
        'name': first.get('name'),
        'address': first.get('vicinity'),
        'latitude': first['geometry']['location']['lat'],
        'longitude': first['geometry']['location']['lng'],
        'place_id': first.get('place_id'),
        'phone': '',
    }
    # Additional Place Details call could get phone, but skipped for brevity
    return station


def _find_nearest_with_nominatim(lat, lon):
    # Nominatim does not have a 'nearby search' endpoint similar to Places
    # We'll query for 'police' and rely on ranked results near the provided coords
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': 'police',
        'format': 'json',
        'limit': 5,
        'addressdetails': 1,
        'extratags': 1,
    }
    resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        return None
    # Choose the nearest by calculating simple distance (approx)
    def dist(r):
        try:
            lat2 = float(r.get('lat'))
            lon2 = float(r.get('lon'))
            return (lat - lat2)**2 + (lon - lon2)**2
        except Exception:
            return 999999
    best = min(results, key=dist)
    station = {
        'name': best.get('display_name', 'Police Station'),
        'address': best.get('display_name', ''),
        'latitude': float(best.get('lat')),
        'longitude': float(best.get('lon')),
        'place_id': best.get('osm_id'),
        'phone': '',
    }
    return station


def find_nearest_police(lat, lon):
    """Return a dict with station details or None."""
    try:
        if GOOGLE_MAPS_API_KEY:
            return _find_nearest_with_google(lat, lon)
        else:
            return _find_nearest_with_nominatim(lat, lon)
    except Exception as e:
        # Log in real project
        return None


def notify_nearest_police(sos_event, request=None):
    """
    Find nearest police station and create a PoliceStation & PoliceNotification record.
    Optionally, attempt to send details (via external API or email) — here we just store record
    and return the PoliceNotification instance.
    """
    lat = sos_event.latitude
    lon = sos_event.longitude
    # If no lat/lon on the sos_event, try to get from request (if provided) or abort
    if (not lat or not lon) and request:
        # try to read from POST params
        try:
            lat = float(request.POST.get('lat'))
            lon = float(request.POST.get('lon'))
        except Exception:
            pass
    if not lat or not lon:
        # Still no location; create a PoliceNotification with failed status
        payload = json.dumps({'error': 'no location available', 'user': sos_event.user.username})
        pn = PoliceNotification.objects.create(sos_event=sos_event, payload=payload, status='failed', response='No location')
        return pn

    station_data = find_nearest_police(float(lat), float(lon))
    police_station = None
    if station_data:
        police_station, _ = PoliceStation.objects.get_or_create(
            place_id=station_data.get('place_id') or station_data.get('name'),
            defaults={
                'name': station_data.get('name') or 'Police Station',
                'address': station_data.get('address') or '',
                'latitude': station_data.get('latitude'),
                'longitude': station_data.get('longitude'),
                'phone': station_data.get('phone') or '',
            }
        )
    # Build payload with user info
    try:
        profile = sos_event.user.profile
        photo_url = None
        if profile.photo:
            if request:
                photo_url = request.build_absolute_uri(profile.photo.url)
            else:
                photo_url = profile.photo.url
        phone = profile.phone or ''
    except Exception:
        photo_url = ''
        phone = ''

    payload = {
        'user': sos_event.user.username,
        'phone': phone,
        'photo_url': photo_url,
        'message': sos_event.message or 'SOS',
        'latitude': str(lat),
        'longitude': str(lon),
        'time': timezone.now().isoformat(),
    }
    payload_text = json.dumps(payload)
    pn = PoliceNotification.objects.create(
        sos_event=sos_event,
        police_station=police_station,
        payload=payload_text,
        status='sent' if police_station else 'failed',
        response='Station found' if police_station else 'No station found'
    )

    # In a real implementation, here you would POST the payload to the police station API or call an SMS/Email gateway.

    return pn

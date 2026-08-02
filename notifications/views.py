from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import send_location_update, send_notifications_for_sos
from sos.models import SosEvent


@login_required
def update_location(request):
    """Receive periodic location updates and send SMS updates."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'error': 'POST required'}, status=400)
    sos_id = request.POST.get('sos_id') or request.POST.get('id')
    lat = request.POST.get('lat')
    lon = request.POST.get('lon')
    if not sos_id or not lat or not lon:
        return JsonResponse({'status': 'error', 'error': 'missing parameters'}, status=400)
    sos = get_object_or_404(SosEvent, pk=sos_id, user=request.user)
    # update SosEvent location for record
    sos.latitude = lat
    sos.longitude = lon
    sos.save()
    notifs = send_location_update(sos, lat, lon)
    return JsonResponse({'status': 'ok', 'sent': len(notifs)})


@login_required
def send_initial(request):
    """Trigger sending initial SMS notifications for a given sos event id.
    This can be called by sos.trigger_sos after creating the event.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'error': 'POST required'}, status=400)
    sos_id = request.POST.get('sos_id')
    if not sos_id:
        return JsonResponse({'status': 'error', 'error': 'missing sos_id'}, status=400)
    sos = get_object_or_404(SosEvent, pk=sos_id, user=request.user)
    notifs = send_notifications_for_sos(sos)
    return JsonResponse({'status': 'ok', 'sent': len(notifs)})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services import notify_nearest_police
from sos.models import SosEvent


@login_required
def notify(request):
    """Endpoint to trigger police notification for a given sos event (POST: sos_id)"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'error': 'POST required'}, status=400)
    sos_id = request.POST.get('sos_id')
    if not sos_id:
        return JsonResponse({'status': 'error', 'error': 'missing sos_id'}, status=400)
    sos = get_object_or_404(SosEvent, pk=sos_id, user=request.user)
    pn = notify_nearest_police(sos, request)
    return JsonResponse({'status': 'ok', 'police_notification_id': pn.id})


@login_required
def notify_page(request):
    """Simple page to manually trigger police notify (useful for debugging)."""
    return render(request, 'police/notify.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SosEvent
from django.http import JsonResponse

# integrate services
from notifications.services import send_notifications_for_sos
from police.services import notify_nearest_police
from video.services import create_video_session


@login_required
def sos_page(request):
    return render(request, 'sos/sos.html')


@login_required
def trigger_sos(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        event = SosEvent.objects.create(user=request.user, message=message,
                                        latitude=lat or None, longitude=lon or None)
        video_url = ''
        try:
            # Send SMS to contacts (synchronous). In production, push to background worker.
            send_notifications_for_sos(event)
        except Exception as e:
            # log error in real app
            pass
        try:
            # Notify nearest police station
            notify_nearest_police(event, request)
        except Exception:
            pass
        try:
            # Create video session and return meeting URL
            vs = create_video_session(event, user=request.user)
            if vs:
                video_url = vs.meeting_url
        except Exception:
            video_url = ''
        return JsonResponse({'status': 'ok', 'id': event.id, 'video_url': video_url})
    return JsonResponse({'status': 'error'}, status=400)

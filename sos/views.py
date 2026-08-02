from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SosEvent
from django.http import JsonResponse


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
        # TODO: send notifications to contacts / police
        return JsonResponse({'status': 'ok', 'id': event.id})
    return JsonResponse({'status': 'error'}, status=400)

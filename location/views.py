from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import LocationPoint


@login_required
def live_location(request):
    return render(request, 'location/location.html')


@login_required
def save_point(request):
    if request.method == 'POST':
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        if lat and lon:
            LocationPoint.objects.create(user=request.user, latitude=lat, longitude=lon)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

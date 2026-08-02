from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PoliceStation


@login_required
def notify_page(request):
    stations = PoliceStation.objects.all()[:50]
    return render(request, "police/notify.html", {"stations": stations})

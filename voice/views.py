from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .models import VoiceCommand
from .forms import VoiceCommandForm


@login_required
def register_voice(request):
    try:
        obj = VoiceCommand.objects.get(user=request.user)
    except VoiceCommand.DoesNotExist:
        obj = None

    if request.method == 'POST':
        form = VoiceCommandForm(request.POST, instance=obj)
        if form.is_valid():
            vc = form.save(commit=False)
            vc.user = request.user
            vc.save()
            return redirect('profiles:view_profile')
    else:
        form = VoiceCommandForm(instance=obj)
    return render(request, 'voice/register.html', {'form': form, 'existing': obj})


@login_required
def get_command(request):
    # returns JSON with the user's active voice phrase (if any)
    try:
        vc = VoiceCommand.objects.get(user=request.user, active=True)
        return JsonResponse({'phrase': vc.phrase})
    except VoiceCommand.DoesNotExist:
        return JsonResponse({'phrase': ''})

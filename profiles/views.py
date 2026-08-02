from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from voice.models import VoiceCommand


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@login_required
def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    # try to fetch associated voice command
    try:
        vc = VoiceCommand.objects.get(user=request.user)
    except VoiceCommand.DoesNotExist:
        vc = None
    return render(request, 'profiles/profile.html', {'profile': profile, 'voice_command': vc})


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles:view_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

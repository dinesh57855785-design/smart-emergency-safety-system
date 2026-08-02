from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ProfileForm
from .models import Profile


def get_or_create_profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile


@login_required
def profile_view(request):
    profile = get_or_create_profile(request.user)
    needs_review = profile.needs_review()
    return render(request, "profiles/profile.html", {"profile": profile, "needs_review": needs_review})


@login_required
def profile_edit(request):
    profile = get_or_create_profile(request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profiles:view")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profiles/edit_profile.html", {"form": form, "profile": profile})


@login_required
def mark_reviewed(request):
    if request.method == "POST":
        profile = get_or_create_profile(request.user)
        profile.last_reviewed = timezone.now().date()
        profile.save()
        messages.success(request, "Thank you. Your profile review has been recorded.")
    return redirect("profiles:view")

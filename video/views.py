from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import VideoSession


@login_required
def join_session(request, pk):
    session = get_object_or_404(VideoSession, pk=pk)
    # Only allow users or staff to join in this simple implementation
    # Police users can be represented via staff flag or a different user model in future
    return render(request, 'video/room.html', {'session': session})


@login_required
def list_sessions(request):
    sessions = VideoSession.objects.filter(user=request.user)
    return render(request, 'video/list.html', {'sessions': sessions})

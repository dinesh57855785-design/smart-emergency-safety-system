import uuid
from django.conf import settings
from .models import VideoSession


def create_video_session(sos_event, user=None):
    """Create a new VideoSession for the given SosEvent and return it."""
    # Generate a unique room name using UUID and SOS id for traceability
    room_name = f'sos-{sos_event.id}-{uuid.uuid4().hex[:10]}'
    meeting_url = f'https://meet.jit.si/{room_name}'
    vs = VideoSession.objects.create(
        sos_event=sos_event,
        room_name=room_name,
        meeting_url=meeting_url,
        user=user or sos_event.user,
        status='active'
    )
    return vs


def end_video_session(video_session):
    video_session.status = 'ended'
    video_session.save()
    return video_session

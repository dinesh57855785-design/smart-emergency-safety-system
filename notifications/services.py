"""
Notification services: Twilio SMS + email alerts for SOS events.
"""
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import NotificationLog


def _build_alert_message(sos_event, recipient_name=""):
    user = sos_event.user
    profile = getattr(user, "profile", None)
    full_name = profile.full_name if profile and profile.full_name else user.get_username()
    location = sos_event.location_url or "Location unavailable"
    return (
        f"EMERGENCY ALERT: {full_name} has triggered an SOS. "
        f"Live location: {location}. "
        f"Video: {sos_event.video_room_url or 'unavailable'}. "
        f"Time: {sos_event.triggered_at:%Y-%m-%d %H:%M}. "
        f"Please respond immediately."
    )


def send_single_sms(to_number, body):
    """Send an SMS via Twilio. Returns (ok, error)."""
    if not (settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_FROM_NUMBER):
        return False, "Twilio not configured"
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=body, from_=settings.TWILIO_FROM_NUMBER, to=to_number)
        return True, message.sid
    except Exception as e:
        return False, str(e)


def send_sos_sms_alerts(sos_event):
    """Send SMS to all trusted contacts snapshot in the SOS event."""
    body = _build_alert_message(sos_event)
    sent, failed = 0, 0
    for contact in sos_event.notified_contacts.all():
        ok, info = send_single_sms(contact.mobile_number, body)
        contact.sms_sent = ok
        contact.sms_error = "" if ok else info
        contact.save()
        NotificationLog.objects.create(
            user=sos_event.user,
            channel="sms",
            recipient=contact.mobile_number,
            body=body,
            status="sent" if ok else "failed",
            error="" if ok else info,
        )
        sent += 1 if ok else 0
        failed += 0 if ok else 1
    if failed and not sent:
        return "failed: all"
    if failed:
        return f"partial: {sent} sent, {failed} failed"
    return f"sent: {sent} contacts"


def send_sos_email_alerts(sos_event):
    """Send an email alert to the user's own email (and could be extended to contacts)."""
    subject = f"EMERGENCY SOS Alert - {sos_event.user.email}"
    body = _build_alert_message(sos_event)
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [sos_event.user.email], fail_silently=True)
        NotificationLog.objects.create(
            user=sos_event.user, channel="email", recipient=sos_event.user.email,
            subject=subject, body=body, status="sent",
        )
    except Exception as e:
        NotificationLog.objects.create(
            user=sos_event.user, channel="email", recipient=sos_event.user.email,
            subject=subject, body=body, status="failed", error=str(e),
        )

import os
from twilio.rest import Client
from django.conf import settings
from django.utils import timezone
from .models import SMSNotification

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM')


def get_twilio_client():
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return None
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def _send_sms_via_twilio(to, body):
    client = get_twilio_client()
    if not client:
        return {'error': 'Twilio not configured'}
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_FROM,
            to=to,
        )
        return {'sid': getattr(message, 'sid', None), 'status': getattr(message, 'status', 'sent')}
    except Exception as e:
        return {'error': str(e)}


def send_notifications_for_sos(sos_event):
    """
    Send initial SMS notifications to all user's emergency contacts for the SosEvent.
    Returns list of SMSNotification instances.
    """
    user = sos_event.user
    contacts = user.emergency_contacts.all()
    results = []
    # build location URL if available
    loc_text = ''
    if sos_event.latitude and sos_event.longitude:
        loc_text = f"Location: https://www.google.com/maps/search/?api=1&query={sos_event.latitude},{sos_event.longitude}\n"

    message_text = sos_event.message or 'SOS'
    base_msg = f"EMERGENCY from {user.username}\n{message_text}\n{loc_text}"

    for c in contacts:
        to = c.phone
        message = base_msg + f"\nContact: {c.name}"
        notif = SMSNotification.objects.create(
            sos_event=sos_event,
            contact=c,
            to_number=to,
            message=message,
            status='queued'
        )
        # attempt to send
        sent = _send_sms_via_twilio(to, message)
        if sent.get('error'):
            notif.status = 'failed'
            notif.response = sent.get('error')
        else:
            notif.twilio_sid = sent.get('sid')
            notif.status = sent.get('status') or 'sent'
            notif.sent_at = timezone.now()
            notif.response = str(sent)
        notif.save()
        results.append(notif)
    return results


def send_location_update(sos_event, lat, lon):
    """
    Send location update SMS to all contacts. Creates SMSNotification records.
    """
    user = sos_event.user
    contacts = user.emergency_contacts.all()
    results = []
    loc_text = f"Updated location: https://www.google.com/maps/search/?api=1&query={lat},{lon}\n"
    base_msg = f"EMERGENCY UPDATE from {user.username}\n{loc_text}"
    for c in contacts:
        to = c.phone
        message = base_msg + f"Contact: {c.name}"
        notif = SMSNotification.objects.create(
            sos_event=sos_event,
            contact=c,
            to_number=to,
            message=message,
            status='queued'
        )
        sent = _send_sms_via_twilio(to, message)
        if sent.get('error'):
            notif.status = 'failed'
            notif.response = sent.get('error')
        else:
            notif.twilio_sid = sent.get('sid')
            notif.status = sent.get('status') or 'sent'
            notif.sent_at = timezone.now()
            notif.response = str(sent)
        notif.save()
        results.append(notif)
    return results

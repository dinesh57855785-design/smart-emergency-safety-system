# Smart Emergency Safety System

This repository contains a Django project scaffold for a Smart Emergency Safety and Response System.

Overview

The system integrates user accounts, profiles, emergency contacts, one-tap SOS, voice commands, live GPS tracking, SMS notifications (Twilio), police notifications, live video (Jitsi), reports and an admin dashboard.

Apps included:
- accounts
- profiles
- contacts
- voice
- sos
- location
- notifications
- police
- video
- reports
- dashboard

Quick start (development)

1. Create virtualenv and install requirements

   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Set environment variables (development)

   # optional (for Twilio)
   export TWILIO_ACCOUNT_SID=your_sid
   export TWILIO_AUTH_TOKEN=your_token
   export TWILIO_FROM=+1234567890

   # optional (for Google Places)
   export GOOGLE_MAPS_API_KEY=your_google_api_key

   # secret key
   export DJANGO_SECRET_KEY='replace-with-secret'

3. Run migrations and create superuser

   python manage.py migrate
   python manage.py createsuperuser

4. Run development server

   python manage.py runserver

5. Access the app

   - Dashboard: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - Register: /accounts/register/
   - SOS: /sos/
   - Reports: /reports/

Architecture & Flow

When a user triggers SOS (button or voice command):
- SosEvent is created
- User's live GPS location is included
- SMS notifications are sent to emergency contacts via Twilio
- Nearest police station is located and a PoliceNotification created
- A Jitsi Meet video session is created and the meeting link is provided
- Emergency history is stored in the database
- Reports and dashboard will reflect the new data

Notes & Next Steps

- Production deployment should use HTTPS for media, geolocation and microphone features.
- Twilio and Google Maps API keys should be stored securely and never committed to git.
- For heavy traffic, move SMS sending and external API calls to background workers (Celery/RQ).


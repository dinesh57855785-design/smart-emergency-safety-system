# Smart Emergency Safety System

This repository contains a Django project scaffold for a Smart Emergency Safety and Response System.

Apps included:
- accounts
- profiles
- contacts
- sos
- location
- dashboard

Quick start (development):

1. Create virtualenv and install requirements
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Run migrations and create superuser
   python manage.py migrate
   python manage.py createsuperuser

3. Run development server
   python manage.py runserver

Notes:
- Configure MEDIA_ROOT and static files in production
- Add real SMS/video providers when moving to production

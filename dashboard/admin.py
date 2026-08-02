"""Dashboard admin customizations.

This module intentionally avoids re-registering models that are already
registered in their respective apps to prevent AlreadyRegistered errors.
"""
from django.contrib import admin

# No model registrations here to avoid duplicate admin registrations.
# Use each app's own admin.py to manage model admin classes.

from django.contrib import admin
from .models import VoiceCommand


@admin.register(VoiceCommand)
class VoiceCommandAdmin(admin.ModelAdmin):
    list_display = ('user', 'phrase', 'active', 'updated_at')
    search_fields = ('user__username', 'phrase')

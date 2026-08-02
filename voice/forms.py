from django import forms
from .models import VoiceMessage


class VoiceMessageForm(forms.ModelForm):
    class Meta:
        model = VoiceMessage
        fields = ["audio_file", "transcript"]

from django import forms
from .models import VoiceCommand


class VoiceCommandForm(forms.ModelForm):
    class Meta:
        model = VoiceCommand
        fields = ['phrase', 'active']
        widgets = {
            'phrase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. help me now'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

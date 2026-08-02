from django import forms
from .models import TrustedContact


class TrustedContactForm(forms.ModelForm):
    class Meta:
        model = TrustedContact
        fields = ["name", "relationship", "mobile_number"]

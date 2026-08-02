from django import forms
from .models import EmergencyContact


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone', 'relationship']

    def clean(self):
        cleaned = super().clean()
        user = getattr(self, 'user', None)
        if user and user.emergency_contacts.count() >= 10 and not self.instance.pk:
            raise forms.ValidationError('You can only have up to 10 emergency contacts.')
        return cleaned

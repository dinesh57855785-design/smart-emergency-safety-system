from django import forms
from .models import EmergencyContact


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone', 'relationship']

    def clean(self):
        cleaned = super().clean()
        user = getattr(self, 'user', None)
        # Maximum 5 contacts per user
        if user and user.emergency_contacts.count() >= 5 and not self.instance.pk:
            raise forms.ValidationError('You can only have up to 5 emergency contacts.')
        # prevent duplicate phone numbers for the same user
        phone = cleaned.get('phone')
        if phone and user:
            qs = user.emergency_contacts.filter(phone=phone)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('This phone number is already in your emergency contacts.')
        return cleaned

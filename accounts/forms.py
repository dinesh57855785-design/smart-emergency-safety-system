from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from profiles.models import Profile


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=False, help_text='Full name')
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        full_name = self.cleaned_data.get('full_name')
        phone = self.cleaned_data.get('phone')
        user.email = email
        if full_name:
            parts = full_name.strip().split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        if commit:
            user.save()
            # create profile
            Profile.objects.get_or_create(user=user, defaults={'phone': phone or ''})
        return user


class UsernameOrEmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # allow login with email
        if username and password:
            try:
                user_obj = User.objects.get(email__iexact=username)
                username_lookup = user_obj.username
            except User.DoesNotExist:
                username_lookup = username
            self.cleaned_data['username'] = username_lookup
        return super().clean()

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    phone = forms.CharField(max_length=20, required=False, label="Mobile Number")

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")


class PasswordResetRequestForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True)


class PasswordResetConfirmForm(SetPasswordForm):
    pass

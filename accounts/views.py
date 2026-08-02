from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.conf import settings

from .forms import SignUpForm
from .models import User


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_email_verified = False
            user.save()
            _send_verification_email(request, user)
            messages.success(
                request,
                "Account created. Please check your email to verify your account.",
            )
            return redirect("accounts:login")
    else:
        form = SignUpForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "Please verify your email before logging in.")
                return redirect("accounts:login")
            login(request, user)
            return redirect("dashboard:index")
        messages.error(request, "Invalid email or password.")
    return render(request, "accounts/login.html")


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user:
                _send_password_reset_email(request, user)
            messages.success(
                request,
                "If an account with that email exists, a password reset link has been sent.",
            )
            return redirect("accounts:login")
    else:
        form = PasswordResetForm()
    return render(request, "accounts/password_reset.html", {"form": form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset. You can now log in.")
                return redirect("accounts:login")
        else:
            form = SetPasswordForm(user)
        return render(
            request,
            "accounts/password_reset_confirm.html",
            {"form": form, "uidb64": uidb64, "token": token},
        )
    messages.error(request, "The reset link is no longer valid.")
    return redirect("accounts:password_reset")


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.success(request, "Your email has been verified. You can now log in.")
        return redirect("accounts:login")
    messages.error(request, "The verification link is no longer valid.")
    return redirect("accounts:register")


def _send_verification_email(request, user):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verify_url = f"https://{current_site.domain}/accounts/verify-email/{uid}/{token}/"
    send_mail(
        subject="Verify your Smart Emergency System account",
        message=f"Click the link to verify your account: {verify_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


def _send_password_reset_email(request, user):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_url = f"https://{current_site.domain}/accounts/password-reset-confirm/{uid}/{token}/"
    send_mail(
        subject="Reset your Smart Emergency System password",
        message=f"Click the link to reset your password: {reset_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )

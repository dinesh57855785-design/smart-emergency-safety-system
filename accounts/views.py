from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth.models import User
from profiles.models import Profile


def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    scheme = request.scheme
    domain = request.get_host()
    verify_url = f"{scheme}://{domain}{reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})}"
    subject = 'Verify your email for Smart Emergency'
    message = render_to_string('accounts/verify_email_message.txt', {
        'user': user,
        'verify_url': verify_url,
        'site_name': getattr(settings, 'SITE_NAME', 'Smart Emergency'),
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # create user but don't activate yet
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # ensure profile exists
            phone = form.cleaned_data.get('phone')
            Profile.objects.get_or_create(user=user, defaults={'phone': phone or ''})
            send_verification_email(request, user)
            messages.success(request, 'Registration successful. Please check your email to verify your account.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been verified. You can now log in.')
        return render(request, 'accounts/activate_account.html', {'user': user})
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return render(request, 'accounts/activate_account.html', {'user': None})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('dashboard:index')
    return render(request, 'accounts/delete_account.html')

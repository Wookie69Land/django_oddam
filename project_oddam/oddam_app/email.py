from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .tokens import account_activation_token


def send_activation_email(request, user):
    email_to = user.email
    title = 'Aktywuj konto aplikacji Oddam w dobre ręce'
    message = render_to_string('activate_account.html', {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(title, message, settings.DEFAULT_FROM_EMAIL, to=[email_to])
    return email.send(fail_silently=False)


def activate_user(uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    else:
        return False


def send_password_email(request, user):
    email_to = user.email
    title = 'Reset hasła'
    message = render_to_string('reset_message.html', {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(title, message, settings.DEFAULT_FROM_EMAIL, to=[email_to])
    return email.send(fail_silently=False)


def check_token(uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        return user
    else:
        return False


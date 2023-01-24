from __future__ import absolute_import, unicode_literals

# from django.contrib.auth.models import User

from celery import shared_task
from celery.utils.log import get_task_logger

from .email import send_activation_email, send_password_email, contact_email


logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_activation_email_task(request, new_user):
    logger.info("Send activation email")
    return send_activation_email(request, new_user)


@shared_task
def send_password_email_task(request, user):
    logger.info("Send forgotten password email")
    return send_password_email(request, user)


@shared_task
def contact_email_task(name, surname, contact_message):
    logger.info("Send contact form to admins")
    return contact_email(name, surname, contact_message)


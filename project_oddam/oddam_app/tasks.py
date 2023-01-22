from __future__ import absolute_import, unicode_literals

# from django.contrib.auth.models import User

from celery import shared_task
from celery.utils.log import get_task_logger

from .email import send_activation_email


logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_activation_email_task(request, new_user):
    logger.info("Send activation email")
    return send_activation_email(request, new_user)


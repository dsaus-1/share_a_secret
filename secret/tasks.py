from datetime import datetime

import pytz
from celery import shared_task

from config import settings
from secret.models import Secret


@shared_task
def delete_after_view(pk: str):
    """
    Deletes the secret after reading
    """

    secret = Secret.objects.filter(pk=pk).first()
    secret.delete()


@shared_task
def delete_after_lifetime():
    """
    Deletes the secret after the expiration date
    """

    time_now = datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE))
    secrets = Secret.objects.filter(delete_data__lt=time_now)
    for secret in secrets:
        secret.delete()

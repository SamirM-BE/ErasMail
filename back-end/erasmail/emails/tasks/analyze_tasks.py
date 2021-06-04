import time

from celery import shared_task
from ..analyze import fetch_emails

@shared_task
def fetch_emails_task(user, email, app_password, host):
    print("cc3")
    fetch_emails(user, email, app_password, host)
from celery import shared_task, current_task
from ..analyze import fetch_emails

@shared_task
def fetch_emails_task(user, email, app_password, host):
    fetch_emails(current_task, user, email, app_password, host)
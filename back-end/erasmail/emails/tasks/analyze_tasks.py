from celery import shared_task, current_task

from ..models import EmailHeaders, EmailStats
from ..imap.jwzthreading import conversation_threading
from ..imap.fetch import get_emails, get_emails_count
from ..imap.jwzthreading import conversation_threading, make_message
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def fetch_emails_task(user_pk, email, app_password, host):
    current_task.update_state(state='STARTED')

    user = User.objects.get(pk=user_pk)
    
    current_task.update_state(state='PROGRESS', meta={'step':'init'})
    emails_count = get_emails_count(host, email, app_password)

    mail_messages = get_emails(host, email, app_password)
    msglist = []
   
    
    fetched_emails_count = 0
    for mail in mail_messages:
        EmailHeaders.objects.create(
            owner=user,
            **mail,
        )
        msglist.append(make_message(mail))
        fetched_emails_count += 1
        current_task.update_state(state='PROGRESS', meta={'step':'fetch', 'done': fetched_emails_count, 'total': emails_count})

    current_task.update_state(state='PROGRESS', meta={'step':'stats'})
    stats = EmailHeaders.objects.filter(owner=user).get_statistics()
    EmailStats.objects.update_or_create(user=user, defaults=stats)

    current_task.update_state(state='PROGRESS', meta={'step':'threads'})
    threads = conversation_threading(msglist)
    for idx, thread in enumerate(threads):
        folder_uids = thread.get_folder_uid()
        for folder, uid in folder_uids:
            email_header = EmailHeaders.objects.get(
                owner=user, uid=uid, folder=folder
            )
            email_header.thread_id = idx
            email_header.save()
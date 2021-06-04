from .models import EmailHeaders, EmailStats
from .imap.jwzthreading import conversation_threading
from time import time
from .imap.fetch import get_emails
from .imap.jwzthreading import conversation_threading, make_message
from django.contrib.auth import get_user_model

User = get_user_model()

def fetch_emails(user_pk, email, app_password, host):

    print('start imap fetching')
    s1 = time()
    
    user = User.objects.get(pk=user_pk)
    # Get the emails from the service layer
    mail_messages = get_emails(host, email, app_password)

    print('save in the DB')
    msglist = []
    for mail in mail_messages:
        EmailHeaders.objects.create(
            owner=user,
            **mail,
        )
        msglist.append(make_message(mail))

    print('finish db saving', time() - s1)

    s = time()
    stats = EmailHeaders.objects.filter(
        owner=user).get_statistics()
    EmailStats.objects.update_or_create(user=user, defaults=stats)
    print('finish stats', time() - s)

    s = time()
    threads = conversation_threading(msglist)
    print('finish threading', time() - s)

    s = time()
    for idx, thread in enumerate(threads):
        folder_uids = thread.get_folder_uid()
        for folder, uid in folder_uids:
            email_header = EmailHeaders.objects.get(
                owner=user, uid=uid, folder=folder
            )
            email_header.thread_id = idx
            email_header.save()
    print('finish', time() - s, time() - s1)
from celery import shared_task, current_task

import re

from ..serializers import EmailHeadersSerializer
from ..models import EmailHeaders
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def get_threads_task(user_pk):
    current_task.update_state(state='STARTED')

    user = User.objects.get(pk=user_pk)

    emails_threads = EmailHeaders.objects.filter(
            owner=user, thread_id__isnull=False
        ).order_by("received_at")
        
    serializer = EmailHeadersSerializer(emails_threads, many=True)
    threads = {}

    restrip_pat = re.compile(
        """((Re(\[\d+\])?:) | (\[ [^]]+ \])\s*)+""", re.IGNORECASE | re.VERBOSE
    )

    for mail in serializer.data:
        data = threads.get(
            mail["thread_id"],
            {
                "thread_id": mail["thread_id"],
                "subject": "",
                "generated_carbon": 0,
                "carbon_yforecast": 0,
                "size": 0,
                "children": [],
            },
        )

        if not data["subject"]:
            subj = restrip_pat.sub("", mail["subject"])
            # remove space at the beginning. This is exactly the space between RE: and the subject name
            data["subject"] = subj.strip()

        data["generated_carbon"] += mail["generated_carbon"]
        data["carbon_yforecast"] += mail["carbon_yforecast"]
        data["size"] += mail["size"]
        data["children"].append(mail)

        threads[mail["thread_id"]] = data
    
    return {"subject": "Threads", "children": list(threads.values())}
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.db.models.functions import TruncDay, Cast
from django.db.models import Count, Case, When, Value, Min, Avg, F, ExpressionWrapper, FloatField

from datetime import timedelta
from django.utils import timezone

from .imap.fetch import get_all_emails
from .imap.delete import move_to_trash
from .imap.attachments import remove_attachments
from .imap.jwzthreading import conversation_threading
from .utils.pollution import emailPollution

from .models import EmailStats, Newsletter, EmailHeaders, Attachment
from .serializers import EmailHeadersSerializer, EmailStatsSerializer

import re

User = get_user_model()

class EmailView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        email = request.user.email

        # request body
        app_password = request.data['app_password']
        host = request.data['host']

        user = request.user

        EmailHeaders.objects.filter(receiver=user).delete() # This remove all old history if the logout was not done successfully


        try:
            print('start imap fetching')
            mail_messages = get_all_emails(host, email, app_password)
            print('finish imap fetching')

            mailbox_size = 0
            emitted_co2 = 0
            emails_seen_count = 0
            emails_received_count = 0
            received_at_min = timezone.now()

            print('save in the DB')
            for mail in mail_messages:

                if mail.list_unsubscribe :
                    try:
                        unsubscribe = Newsletter.objects.get(receiver=user, sender_email=mail.sender_email)
                        # if the one_click is set we don't change anything because it is the best way to unsubscribe
                        if (not unsubscribe.one_click) and mail.list_unsubscribe_post: 
                            unsubscribe.one_click = True
                            unsubscribe.list_unsubscribe = mail.list_unsubscribe
                            
                            unsubscribe.save()
                        elif (not unsubscribe.one_click) and mail.list_unsubscribe[:6] == "mailto":
                            unsubscribe.one_click = False
                            unsubscribe.list_unsubscribe = mail.list_unsubscribe
                            
                            unsubscribe.save()
                    except Newsletter.DoesNotExist as e:
                        unsubscribe = Newsletter.objects.create(receiver=user, list_unsubscribe=mail.list_unsubscribe
                        ,
                                                                one_click=mail.list_unsubscribe_post, sender_email=mail.sender_email)
                    except Newsletter.MultipleObjectsReturned as e:
                        print(f'Multiple objects Newsletter returned\nError from Django = {e}')
                else:
                    unsubscribe = None

                co2 = emailPollution(mail.size, mail.received_at)

                if mail.received_at < received_at_min:
                    received_at_min = mail.received_at

                mailbox_size += mail.size
                emitted_co2 += co2
                emails_seen_count += mail.seen
                emails_received_count += mail.received

                email_headers_model = EmailHeaders.objects.create(
                    uid=mail.uid,
                    seen=mail.seen,
                    subject=mail.subject,
                    sender_name=mail.sender_name,
                    sender_email=mail.sender_email,
                    receiver=user,
                    size=mail.size,
                    received_at=mail.received_at,
                    message_id=mail.message_id,
                    folder=mail.folder,
                    unsubscribe=unsubscribe,
                    co2=co2
                )

                [
                    Attachment.objects.create(
                        email_header=email_headers_model, name=name, size=size
                    )
                    for name, size in mail.attachments
                ]

            print('start stats')
            EmailStats.objects.update_or_create(
                user=user,
                defaults={
                    'mailbox_size': mailbox_size,
                    'emitted_co2': emitted_co2,
                    'emails_count': len(mail_messages),
                    'emails_seen_count': emails_seen_count,
                    'emails_received_count': emails_received_count,
                    'months_since_creation': (timezone.now() - received_at_min).days / (365.25/12)
                }
            )
            print('finish stats')

            print('start threading')
            threads = conversation_threading(mail_messages)
            print('finish threading')

            print('update DB with threads')
            for idx, thread in enumerate(threads):  # imporove with a generator
                folder_uids = thread.get_folder_uid()
                for folder, uid in folder_uids:
                    email_header = EmailHeaders.objects.get(receiver=user, uid=uid, folder=folder)
                    email_header.thread_id = idx
                    email_header.save()
            print('finish')

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        email = request.user.email
        user = request.user

        # request body
        app_password = request.data.get('app_password', None)
        host = request.data.get('host', None)
        folder_uids = request.data.get('uids', False)
        # uids template
        # "uids": {
        #     "INBOX":[3, 5],
        #     "SENT" :[14, 53],
        #     }
        if folder_uids:
            move_to_trash(host, email, app_password, folder_uids)
            [[EmailHeaders.objects.get(receiver=user, folder=folder_name, uid=uid).delete() for uid in uids] for folder_name, uids in folder_uids.items()]
        else:
            EmailHeaders.objects.filter(receiver=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Attachments(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        email = request.user.email
        user = request.user

        # request body
        app_password = request.data.get("app_password", None)
        host = request.data.get("host", None)
        folder_uids = request.data.get("uids", False)
        # uids template
        # "uids": {
        #     "INBOX":[3, 5],
        #     "SENT" :[14, 53],
        #     }
        if folder_uids:
            remove_attachments(host, email, app_password, folder_uids)
            [
                [
                    Attachment.objects.filter(
                        email_header__receiver=user, email_header__folder=folder_name, email_header__uid=uid
                    ).delete()
                    for uid in uids
                ]
                for folder_name, uids in folder_uids.items()
            ]

        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        emails_threads = EmailHeaders.objects.filter(
            receiver=user, thread_id__isnull=False
        ).order_by('received_at')

        serializer = EmailHeadersSerializer(emails_threads, many=True)
        threads = {}

        restrip_pat = re.compile(
            """((Re(\[\d+\])?:) | (\[ [^]]+ \])\s*)+""", re.IGNORECASE | re.VERBOSE)

        for mail in serializer.data:

            data = threads.get(mail["thread_id"], {
                'subject': '',
                'co2': 0,
                'size': 0,
                'children': [],
            })

            if not data['subject']:
                subj = restrip_pat.sub('', mail['subject'])
                # remove space at the beginning. This is exactly the space between RE: and the subject name
                data['subject'] = subj.strip()

            data['co2'] += mail['co2']
            data['size'] += mail['size']
            data['children'].append(mail)

            threads[mail["thread_id"]] = data

        response = {'subject': 'Threads', 'children': threads.values()}

        return Response(data=response, status=status.HTTP_200_OK)


class Statistics(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, kind):
    
        if kind == 'user':
            user = request.user

            before_than = request.data.get("before_than", 0)
            ligher_than = request.data.get("ligher_than", 1e6)

            # generate statistics based on EmailHeaders: these stats aren't persistents
            all_emails = EmailHeaders.objects.filter(receiver=user)
            email_header_stats = all_emails.aggregate(
                threads_count=Count('thread_id', distinct=True),
                emails_before_count=Count(Case(When(received_at__lte=timezone.now() - timedelta(days=before_than*365), then=Value(1)))),
                emails_lighter_count=Count(Case(When(size__lte=ligher_than, then=Value(1))))
            )

            # generate statistics based on Newsletter
            all_newsletters = Newsletter.objects.filter(receiver=user)
            newsletter_stats = all_newsletters.aggregate(
                newsletters_count=Count('pk'),
                unsubscribed_newsletters_count=Count(
                    Case(When(unsubscribed=True, then=Value(1)))),
            )

            # generate statistics based on EmailStats
            email_stats = EmailStatsSerializer(EmailStats.objects.get(user=user)).data

            # merge all statistics
            response = {
                **email_stats,
                **email_header_stats,
                **newsletter_stats
                }
        elif kind == 'erasmail':
            # generate average users statistics based on EmailStats
            average_users_stats = EmailStats.objects.annotate(
                emails_received_rate=ExpressionWrapper(F('emails_received_count') / F('months_since_creation'), output_field=FloatField()),
                emails_send_rate=ExpressionWrapper((F('emails_count') - F('emails_received_count'))/ F('months_since_creation'), output_field=FloatField()),
                open_rate=ExpressionWrapper(F('emails_seen_count') / Cast(F('emails_count'), output_field=FloatField()), output_field=FloatField()),
            ).aggregate(
                average_mailbox_size=Avg('mailbox_size'),
                average_emitted_co2=Avg('emitted_co2'),
                average_saved_co2=Avg('saved_co2'),
                average_emails_received_rate=Avg('emails_received_rate'),
                average_emails_send_ratet=Avg('emails_send_rate'),
                average_open_rate = Avg('open_rate'),
            )
            response = average_users_stats
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=response, status=status.HTTP_200_OK)

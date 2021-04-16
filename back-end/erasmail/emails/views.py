import re
from datetime import timedelta
import requests
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from .imap.attachments import remove_attachments
from .imap.delete import move_to_trash
from .imap.fetch import get_emails
from .imap.newsletters import send_email, delete_unsub_email
from .imap.jwzthreading import conversation_threading
from .models import EmailHeaders, EmailStats, Newsletter

from django.db.models import F

from .serializers import (
    EmailHeadersSerializer,
    EmailStatsSerializer,
    NewsletterSerializer,

)


User = get_user_model()

class BasicPagination(PageNumberPagination):
    page_size = 10

from time import time

class EmailView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = BasicPagination
    serializer_class = EmailHeadersSerializer

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def post(self, request):
        email = request.user.email

        # request body
        app_password = request.data.get("app_password", "")
        host = request.data.get("host", "")

        user = request.user

        # Remove all old history if the logout was not done successfully
        EmailHeaders.objects.filter(receiver=user).delete()

        try:
            print('start imap fetching')
            s1 = time()
            # Get the emails from the service layer
            mail_messages = get_emails(host, email, app_password)
            print('finish imap fetching', time() - s1)

            print('save in the DB')
            s = time()
            [
                EmailHeaders.objects.create(
                    receiver=user,
                    **mail,
                )
                for mail in mail_messages
            ]

            print('finish db saving', time() - s)

            print('start stats')
            s = time()
            stats = EmailHeaders.objects.filter(
                receiver=user).get_statistics()
            EmailStats.objects.update_or_create(user=user, defaults=stats)
            print('finish stats', time() - s)

            print('start threading')
            s = time()
            threads = conversation_threading(mail_messages)
            print('finish threading', time() - s)

            print('update DB with threads')
            s = time()
            for idx, thread in enumerate(threads):  # imporove with a generator
                folder_uids = thread.get_folder_uid()
                for folder, uid in folder_uids:
                    email_header = EmailHeaders.objects.get(
                        receiver=user, uid=uid, folder=folder
                    )
                    email_header.thread_id = idx
                    email_header.save()
            print('finish', time() - s, time() - s1)

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        before_than = int(request.query_params.get("before_than", 0))
        greater_than = int(request.query_params.get("greater_than", 0))  # in MB
        seen = request.query_params.get("seen") == "true"
        selected_filters = request.query_params.getlist("selected_filters[]")

        folder = request.query_params.get("folder")

        user = request.user

        emails_headers = EmailHeaders.objects.filter(receiver=user)

        if before_than:
            emails_headers = emails_headers.filter(
                received_at__lte=timezone.now() - timedelta(days=int(before_than*365.25)))
        if greater_than:
            emails_headers = emails_headers.filter(size__gte=greater_than*1e6)
        if not seen:
            emails_headers = emails_headers.filter(seen=seen)
        if folder:
            emails_headers = emails_headers.filter(folder__iexact=folder)
        if selected_filters:
            # sender_emails = [
            #     # emails to yourself
            #     # 'amazon',
            #     # 'aliexpress',
            #     # 'zoom',
            #     # 'uber',
            # ]
            try:
                emails_headers = emails_headers.apply_filters(selected_filters)
            except AttributeError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        emails_headers = emails_headers.order_by('-received_at')

        carbon_data = emails_headers.get_carbon_stats()

        page = self.paginate_queryset(emails_headers)
        if page is not None:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(emails_headers, many=True)

        data = {**carbon_data, **serializer.data}
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        email = user.email

        # request body
        app_password = request.data.get("app_password", None)
        host = request.data.get("host", None)
        folder_uids = request.data.get("uids", False)
        pks = request.data.get("pks", False)

        stats_to_update = request.data.get("stats_to_update", False)
        if folder_uids and pks:
            move_to_trash(host, email, app_password, folder_uids)
            emails_headers = EmailHeaders.objects.filter(pk__in=pks)
            email_stats = user.emailstats

            #Success need some stats to be updated, like nb of deleted emails through smart filters
            if stats_to_update:
                deleted_cnt = emails_headers.count() # nb of deleted emails
                updated_success_stats = {statistic: deleted_cnt for statistic in stats_to_update}
                email_stats.add(**updated_success_stats)

            emails_headers_stats = emails_headers.get_statistics()
            emails_headers.delete()
            email_stats.update_deleted_email(emails_headers_stats)
            email_stats.save()
        else:
            EmailHeaders.objects.filter(receiver=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FolderView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        folders = EmailHeaders.objects.filter(
            receiver=user).values_list('folder', flat=True).distinct()
        return Response(data=folders, status=status.HTTP_200_OK)


class AttachmentView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        user = request.user
        email = user.email

        # request body
        app_password = request.data.get("app_password", None)
        host = request.data.get("host", None)
        folder_uids = request.data.get("uids", False)
        pks = request.data.get("pks", False)
        # uids template
        # "uids": {
        #     "INBOX":[3, 5],
        #     "SENT" :[14, 53],
        #     }
        uids_cnt = 0
        for folder in folder_uids:
            uids_cnt += len(folder_uids[folder]) # get nb of emails to delete
        EmailStats.objects.update(deleted_attachments_count=F('deleted_attachments_count')+uids_cnt)

        if folder_uids and pks:
            remove_attachments(host, email, app_password, folder_uids)
            email_stats = user.emailstats
            emails_headers = EmailHeaders.objects.filter(pk__in=pks)
            for folder_name, uids in folder_uids.items():
                emails_headers_folder = emails_headers.filter(
                    folder=folder_name)
                for uid in uids:
                    email_header = emails_headers_folder.get(uid=uid)
                    attachments = email_header.attachments.all()
                    attachments_stats = attachments.get_attachment_stats()
                    attachments.delete()
                    email_stats.update_deleted_attachments(attachments_stats)
                    email_header.update_deleted_attachments(attachments_stats)
                    email_stats.save()
                    email_header.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailHeadersSerializer

    def get(self, request):
        user = request.user

        emails_threads = EmailHeaders.objects.filter(
            receiver=user, thread_id__isnull=False
        ).order_by("received_at")

        serializer = self.serializer_class(emails_threads, many=True)
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
                    "size": 0,
                    "children": [],
                },
            )

            if not data["subject"]:
                subj = restrip_pat.sub("", mail["subject"])
                # remove space at the beginning. This is exactly the space between RE: and the subject name
                data["subject"] = subj.strip()

            data["generated_carbon"] += mail["generated_carbon"]
            data["size"] += mail["size"]
            data["children"].append(mail)

            threads[mail["thread_id"]] = data

        response = {"subject": "Threads", "children": threads.values()}

        return Response(data=response, status=status.HTTP_200_OK)


class ThreadDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailHeadersSerializer

    def get(self, request, thread_id):
        user = request.user

        emails_threads = EmailHeaders.objects.filter(
            receiver=user, thread_id=thread_id
        ).order_by("received_at")

        serializer = self.serializer_class(emails_threads, many=True)

        restrip_pat = re.compile(
            """((Re(\[\d+\])?:) | (\[ [^]]+ \])\s*)+""", re.IGNORECASE | re.VERBOSE
        )

        subject = restrip_pat.sub("", serializer.data[0]["subject"]).strip()

        stats = emails_threads.aggregate(
            generated_carbon=Sum("generated_carbon"),
            size=Sum("size"),
        )

        response = {
            "thread_id": thread_id,
            "subject": subject,
            **stats,
            "children": serializer.data,
        }

        return Response(data=response, status=status.HTTP_200_OK)


class Statistics(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, kind):
        user = request.user

        if kind == "user":

            before_than = int(request.query_params.get("before_than", 0))
            larger_than = float(request.query_params.get("larger_than", 0))

            # generate statistics based on EmailHeaders: these stats aren't persistents
            emails_headers = EmailHeaders.objects.filter(receiver=user)
            email_header_stats = {
                ** emails_headers.get_stats_unseen_emails(),
                ** emails_headers.get_thread_stats(),
                ** emails_headers.get_stats_before_than(before_than),
                ** emails_headers.get_stats_larger_than(larger_than),
            }

            # generate statistics based on Newsletter
            newsletters = Newsletter.objects.filter(receiver=user)
            newsletter_stats = newsletters.get_newsletter_stats()

            # generate statistics based on EmailStats
            email_stats = EmailStatsSerializer(
                EmailStats.objects.get(user=user)).data

            # merge all statistics
            response = {**email_stats, **
                        email_header_stats, **newsletter_stats}
        elif kind == "users":
            users_stats = EmailStats.objects.all().with_score().order_by('-score')
            
            users_stats_serializer = EmailStatsSerializer(users_stats, many=True).data
            current_user_id = users_stats.get(user=user).pk

            response = {
                'users_stats':users_stats_serializer,
                'current_user_id': current_user_id,
                }
        elif kind == "erasmail":
            # generate average users statistics based on EmailStats
            response = EmailStats.objects.get_general_stats()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=response, status=status.HTTP_200_OK)

    # def put(self, request, kind):
    #     user = request.user

    #     if kind==''


class NewsletterListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        newsletters = (
            Newsletter.objects.filter(receiver=user)
            .with_email_counter()
            .with_seen_email_counter()
            .with_avg_daily_emails()
            .with_carbon().order_by('-avg_daily_emails')
        )

        serializer = NewsletterSerializer(newsletters, many=True)
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        senders = request.data.get("senders", None) #TODO: check if PK better than senders
        host= request.data["host"]
        app_password = request.data["app_password"]

        email_stats = user.emailstats

        uids_to_delete = request.data.get("uids_to_delete", {})
        uids_cnt = 0
        for folder in uids_to_delete:
            uids_cnt += len(uids_to_delete[folder]) # get nb of emails to delete

        email_stats.add(newsletters_deleted_emails_count=uids_cnt)
        email_stats.save()

        move_to_trash(host, user.email, app_password, uids_to_delete)
        Newsletter.objects.filter(receiver=user, sender_email__in=senders).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


    # unsubscribe from one-lick links
    @api_view(['POST']) #TODO: temporary, should be @action with viewset
    def unsubscribe(request):

        user = request.user
        unsubscribe_type = request.data.get("unsubscribe_type", "")
        pk = request.data["id"]

        Newsletter.objects.filter(pk=pk).update(unsubscribed=True)
        EmailStats.objects.filter(user=user).update(unsubscribed_newsletters_count=F('unsubscribed_newsletters_count')+1)
        if unsubscribe_type == "oneclick":
            url = request.data.get("url", "")
            req = requests.post(url, data = {'List-Unsubscribe':'One-Click'}) # confirm data
            if req.status_code == 200:
                return Response(status=status.HTTP_200_OK)

        elif unsubscribe_type == "mailto":
            to = request.data.get("to", "")
            subject = request.data.get("subject", "")
            host= request.data["host"] #TODO: !!!CAREFUL!!! : STMP host != host
            app_password = request.data["app_password"]
            send_email(sender=user.email, smtp_host=host, password=app_password, to=to, subject=subject)
            delete_unsub_email(host=host, sender=user.email, password=app_password, to=to)
            return Response(status=status.HTTP_200_OK)
        else:
            print("open browser")

        return Response(status.HTTP_400_BAD_REQUEST)


        

    # def delete(self, request):
    #     user = request.user
    #     host= request.data["host"]
    #     app_password = request.data["app_password"]

    #     Newsletter.objects.filter(receiver=user, sender_email__in=senders).delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)


    
    # @api_view(['POST']) 
    # def unsubscribe(request):

    #     user = request.user
       
    #     return Response(status=status.HTTP_200_OK)
    #     return Response(status.HTTP_400_BAD_REQUEST)


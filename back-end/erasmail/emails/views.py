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
from .imap.newsletters import send_email, delete_unsub_email
from .models import EmailHeaders, EmailStats, Newsletter

from django.db.models import F

from .serializers import (
    EmailHeadersSerializer,
    EmailStatsSerializer,
    NewsletterSerializer,
)

from celery.result import AsyncResult
from .tasks.analyze_tasks import fetch_emails_task

User = get_user_model()

class BasicPagination(PageNumberPagination):
    page_size = 10

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
        EmailHeaders.objects.filter(owner=user).delete()

        task_analyze = fetch_emails_task.delay(user.pk, email, app_password, host)
        return Response(data={"task_id": task_analyze.id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        before_than = int(request.query_params.get("before_than", 0))
        greater_than = int(request.query_params.get("greater_than", 0))  # in MB
        seen = request.query_params.get("seen") == "true"
        selected_filters = request.query_params.getlist("selected_filters[]")

        ordered_by = request.query_params.get("ordered_by")
        folder = request.query_params.get("folder")

        task_id = request.query_params.get("task_id")
        if task_id:
            result = AsyncResult(id=task_id, app=fetch_emails_task)
            return Response(data = {"state": result.state, "info": result.info}, status=status.HTTP_200_OK)

        user = request.user
        emails_headers = EmailHeaders.objects.filter(owner=user)

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
            try:
                emails_headers = emails_headers.apply_filters(selected_filters)
            except AttributeError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        emails_headers = emails_headers.order_by(ordered_by)

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
            EmailHeaders.objects.filter(owner=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FolderView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        folders = EmailHeaders.objects.filter(
            owner=user).values_list('folder', flat=True).distinct()
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
        EmailStats.objects.update(deleted_attachments=F('deleted_attachments')+uids_cnt)

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
            owner=user, thread_id__isnull=False
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

        response = {"subject": "Threads", "children": threads.values()}

        return Response(data=response, status=status.HTTP_200_OK)


class ThreadDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailHeadersSerializer

    def get(self, request, thread_id):
        user = request.user

        emails_threads = EmailHeaders.objects.filter(
            owner=user, thread_id=thread_id
        ).order_by("received_at")

        serializer = self.serializer_class(emails_threads, many=True)

        restrip_pat = re.compile(
            """((Re(\[\d+\])?:) | (\[ [^]]+ \])\s*)+""", re.IGNORECASE | re.VERBOSE
        )

        subject = restrip_pat.sub("", serializer.data[0]["subject"]).strip()

        stats = emails_threads.aggregate(
            carbon_yforecast=Sum("carbon_yforecast"),
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
            statistics = {}
            emails_stats = {} # general statistics about emails (e.g. unread emails, received emails, ...)
            newsletters_stats = {} # general statistics about newsletters (e.g. nb of newsletters, ..)
            threads_stats = {} # general statistics about threads (e.g. nb of threads, ...)
            erasmail_stats = {} # statistics about erasmail usage (e.g. nb of deleted emails trough a certain feature, )
            emailbox_stats = {} # statistics about the mailbox (e.g. size, carbon, ...)

            # generate statistics based on EmailHeaders: these stats aren't persistent
            emails_headers = EmailHeaders.objects.filter(owner=user)
            # generate statistics based on EmailStats
            email_stats_data = EmailStatsSerializer(EmailStats.objects.get(user=user)).data
            emails_stats = {
                "emails_count" : email_stats_data['emails_count'],
                "received" : email_stats_data['received'],
                "read" : email_stats_data['read'],
                ** emails_headers.get_unseen_emails_stats(),
                ** emails_headers.get_older_3Y_stats(),
                ** emails_headers.get_larger_1MB_stats(),
                ** emails_headers.get_useless_stats(),
            }

            newsletters = Newsletter.objects.filter(receiver=user)
            newsletters_stats = {
                ** newsletters.get_newsletters_stats(),
            }

            threads_stats = {
                ** emails_headers.get_threads_stats(),
            }

            erasmail_stats = {
                "deleted_emails": email_stats_data['deleted_emails'],
                "deleted_emails_older_filter" : email_stats_data['deleted_emails_older_filter'],
                "deleted_emails_larger_filter" : email_stats_data['deleted_emails_larger_filter'],
                "deleted_emails_useless_filter" : email_stats_data['deleted_emails_useless_filter'],
                "deleted_emails_threads_feature" : email_stats_data['deleted_emails_threads_feature'],
                "deleted_emails_newsletters_feature" : email_stats_data['deleted_emails_newsletters_feature'],
                "unsubscribed_newsletters" : email_stats_data['unsubscribed_newsletters'],
                "deleted_attachments" : email_stats_data['deleted_attachments'],
                "shared_badges" : email_stats_data['shared_badges'],
                "shared_stats" : email_stats_data['shared_stats'],
                "saved_carbon"  : email_stats_data['saved_carbon'],
            }

            emailbox_stats = {
                "emailbox_size" : email_stats_data['emailbox_size'],
                "carbon" : email_stats_data['emailbox_carbon'],
                "carbon_forecast" : email_stats_data['emailbox_carbon_forecast'],
                "initial_carbon" : email_stats_data['emailbox_initial_carbon'],
                "created_since_months" : email_stats_data['created_since_months'],
            }

            statistics = {
                "emails" : emails_stats,
                "newsletters" : newsletters_stats,
                "threads" : threads_stats,
                "erasmail" : erasmail_stats,
                "emailbox" : emailbox_stats,
            }

            response = statistics
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


class NewsletterListView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = BasicPagination
    serializer_class = NewsletterSerializer

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


    def get(self, request):
        user = request.user

        newsletters = (
            Newsletter.objects.filter(receiver=user)
            .with_email_counter()
            .with_seen_email_counter()
            .with_avg_daily_emails()
            .with_carbon().order_by('-avg_daily_emails')
        )

        carbon_data = newsletters.get_carbon_stats()

        page = self.paginate_queryset(newsletters)
        if page is not None:
            serializer = self.get_paginated_response(
            self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(newsletters, many=True)

        data = {**carbon_data, **serializer.data}
        return Response(data, status=status.HTTP_200_OK)

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

        email_stats.add(deleted_emails_newsletters_feature=uids_cnt, deleted_emails=uids_cnt)
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
        EmailStats.objects.filter(user=user).update(unsubscribed_newsletters=F('unsubscribed_newsletters')+1)
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
            smtp_host = request.data.get("smtp_host", host)
            smtp_port = request.data.get("smtp_port", 587)
            print(smtp_host, "aaaaaaaaaa")
            print(smtp_port, "aaaaaaaaaa")
            send_email(sender=user.email, smtp_host=smtp_host, smtp_port=smtp_port, password=app_password, to=to, subject=subject)
            delete_unsub_email(host=host, sender=user.email, password=app_password, to=to)
            return Response(status=status.HTTP_200_OK)
        else:
            print("open browser")

        return Response(status.HTTP_400_BAD_REQUEST)
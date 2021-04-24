from rest_framework import serializers

from .models import Attachment, EmailHeaders, EmailStats, Newsletter
from django.utils import timezone

from datetime import timedelta


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        exclude = ('id', 'email_header')

class EmailHeadersSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    is_received = serializers.SerializerMethodField(
        "get_is_received",
        read_only=True,
    )

    def get_is_received(self, obj):
        try:
            return obj.owner.email == obj.receiver_email
        except:
            print('hello')
            return False

    class Meta:
        model = EmailHeaders
        exclude = ('owner', 'unsubscribe')

class NewsletterSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField(
        "get_sender_name",
        read_only=True,
    )
    emails_cnt = serializers.IntegerField(
        read_only=True,
        help_text="nb of stored emails",
    )
    seen_emails_cnt = serializers.IntegerField(
        read_only=True,
    )
    avg_daily_emails = serializers.FloatField(
        read_only=True,
        help_text="average daily nb of emails received",
    )
    received_at = serializers.SerializerMethodField(
        "get_received_at",
        read_only=True,
        help_text="Last time that an email was received",
    )
    generated_carbon = serializers.FloatField(
        read_only=True,
        help_text="generated co2 until now",
    )
    forecasted_carbon = serializers.FloatField(
        read_only=True,
        help_text="forecast co2 one year from now",
    )

    uids_folders = serializers.SerializerMethodField("get_uids_folder")

    def get_sender_name(self, obj):
        try:
            return obj.email_headers.first().sender_name
        except:
            return ""

    def get_received_at(self, obj):
        try:
            return obj.get_latest_email().received_at.date()
        except:
            return timezone.now() - timedelta(weeks=4800)

    def get_uids_folder(self, obj):
        uids_folder = {}
        for email in obj.email_headers.all():
            uids_folder.setdefault(email.folder,[]).append(email.uid)
        return uids_folder

    class Meta:
        model = Newsletter
        exclude = ["receiver"]


class EmailStatsSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField(
        "get_nickname",
        read_only=True,
    )

    score = serializers.SerializerMethodField(
        "get_score",
        read_only=True,
    )

    def get_nickname(self, obj):
        try:
            return obj.user.nickname
        except:
            return ""

    def get_score(self, obj):
        try:
            return obj.score
        except:
            return 0

    class Meta:
        model = EmailStats
        exclude = ["user"]



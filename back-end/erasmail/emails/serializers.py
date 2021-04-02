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

    class Meta:
        model = EmailHeaders
        exclude = ('id', 'receiver', 'message_id', 'unsubscribe')

class NewsletterSerializer(serializers.ModelSerializer):
    # get sender_name from related model (emailheaders)
    # sender_name = serializers.SlugRelatedField(many=True, slug_field='sender_name', read_only=True, source="newsletters")
    sender_email = serializers.SerializerMethodField('get_sender_email', read_only=True, )
    emails_cnt = serializers.IntegerField(read_only=True, help_text="nb of stored emails", )
    seen_emails_cnt = serializers.IntegerField(read_only=True, )
    avg_daily_emails = serializers.FloatField(read_only=True, help_text="average daily nb of emails received", )
    received_at = serializers.SerializerMethodField('get_received_at', read_only=True, help_text="Last time that an email was received", )
    generated_carbon = serializers.FloatField(read_only=True, help_text="generated co2 until now", )
    forecasted_carbon = serializers.FloatField(read_only=True, help_text="forecast co2 one year from now", )
    emails_uids = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        source='newsletters',
        slug_field='uid'
     )


    def get_sender_email(self, obj):
        try :
            return obj.newsletters.first().sender_name
        except :
            return ''

    def get_received_at(self, obj):
        try :
            return obj.get_latest_email().received_at.date()
        except :
            return timezone.now() - timedelta(weeks=4800)

    class Meta:
        model = Newsletter
        exclude = ('id','receiver')

class EmailStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailStats
        exclude = ('id','user')

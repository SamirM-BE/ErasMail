from django.db.models import fields
from rest_framework import serializers
from .models import EmailHeaders, Newsletter, Attachment

class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        exclude = ('id', 'email_header')

class EmailHeadersSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = EmailHeaders
        exclude = ('id', 'receiver', 'message_id')


class NewsletterSerializer(serializers.ModelSerializer):
    receiver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Newsletter
        exclude = ('id',)


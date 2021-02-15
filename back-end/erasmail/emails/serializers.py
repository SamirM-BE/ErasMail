from rest_framework import serializers
from .models import EmailHeaders, Newsletter, Reference, Attachment, InReplyTo

class EmailHeadersSerializer(serializers.ModelSerializer):
    receiver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = EmailHeaders
        exclude = ('id',)


class NewsletterSerializer(serializers.ModelSerializer):
    receiver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Newsletter
        exclude = ('id',)


class ReferenceSerializer(serializers.ModelSerializer):
    email_header = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reference
        exclude = ('id',)


class AttachmentSerializer(serializers.ModelSerializer):
    email_header = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Attachment
        exclude = ('id',)

class InReplyToSerializer(serializers.ModelSerializer):
    email_header = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = InReplyTo
        exclude = ('id',)
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class EmailHeaders(models.Model):
    uid = models.IntegerField(unique=True)
    seen = models.BooleanField(default=False)
    subject = models.CharField(max_length=255, blank=True)
    sender_name = models.CharField(max_length=255, blank=True)
    sender_email = models.EmailField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField()
    received_at = models.DateTimeField()
    message_id = models.CharField(max_length=255)
    folder = models.CharField(max_length=255)

    def __str__(self):
        return f'from: {self.sender}\nto: {self.receiver}\nsubject: {self.subject}'

class Attachment(models.Model):
    email_header = models.ForeignKey(EmailHeaders, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    size = models.IntegerField()

class Reference(models.Model):
    email_header = models.ForeignKey(EmailHeaders, on_delete=models.CASCADE)
    reference = models.CharField(max_length=255)

class InReplyTo(models.Model):
    email_header = models.ForeignKey(EmailHeaders, on_delete=models.CASCADE)
    in_reply_to = models.CharField(max_length=255)

class Newsletter(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    # list_unsubscribe_type = models.CharField(max_length=255)

    list_unsubscribe = models.CharField(max_length=255)
    one_click = models.BooleanField(default=False)
    unsubscribed = models.BooleanField(default=False)
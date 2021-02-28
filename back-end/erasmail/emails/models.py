from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Newsletter(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    list_unsubscribe = models.CharField(max_length=5000)
    one_click = models.BooleanField(default=False)
    unsubscribed = models.BooleanField(default=False)
    sender_email = models.EmailField()

    def __str__(self) -> str:
        return f'pk: {self.pk}  sender: {self.sender_email}'

class EmailHeaders(models.Model):

    uid = models.IntegerField()
    seen = models.BooleanField(default=False)
    subject = models.CharField(max_length=5000, blank=True)
    sender_name = models.CharField(max_length=5000, blank=True)
    sender_email = models.EmailField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField(default=0)
    received_at = models.DateTimeField(null=True)
    message_id = models.CharField(max_length=5000)
    folder = models.CharField(max_length=5000)
    thread_id = models.IntegerField(null=True)

    unsubscribe = models.ForeignKey(Newsletter, related_name='newsletters', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'from: {self.sender_email}\nto: {self.receiver}\nsubject: {self.subject}'

class Attachment(models.Model):
    email_header = models.ForeignKey(EmailHeaders, related_name='attachments', on_delete=models.CASCADE)
    name = models.CharField(max_length=5000)
    size = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.size}'

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from .managers import (NewsletterQuerySet, EmailStatsQuerySet, EmailHeadersQuerySet, AttachmentQuerySet, )
from .utils.pollution import emailPollution, getYearlyCarbonForecast

User = get_user_model()

class EmailStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emailbox_size = models.PositiveIntegerField(null=False, help_text="Emailbox current size (bytes)")
    emailbox_initial_carbon = models.FloatField(null=False, validators=[MinValueValidator(0.0)], help_text="Carbon equivalent of the emailbox at the first connection ever")
    emailbox_carbon = models.FloatField(null=False, default=0, validators=[MinValueValidator(0.0)], help_text="Emailbox current carbon equivalent")
    emailbox_carbon_forecast = models.FloatField(null=False, default=0, validators=[MinValueValidator(0.0)], help_text="Forecast of the emailbox yearly pollution")
    emails_count  =  models.PositiveIntegerField(null=False)
    read = models.PositiveIntegerField(null=False)
    received = models.PositiveIntegerField(null=False)
    created_since_months = models.FloatField(null=False, validators=[MinValueValidator(0.0)], help_text="Number of months since creation of email account, based on first stored received email")
    saved_carbon = models.FloatField(default=0, validators=[MinValueValidator(0.0)], help_text="Total saved carbon by the current user")
    shared_badges = models.PositiveIntegerField(default=0, help_text="The user has shared his badges on social media")
    shared_stats = models.PositiveIntegerField(default=0, help_text="The user has shared his stats on social media")
    unsubscribed_newsletters = models.PositiveIntegerField(default=0, help_text="Number of newsletters that have been unsubscribed using ErasMail") #TODO: on calcule déjà cette valeur faut juste l'insérer.
    deleted_emails = models.PositiveIntegerField(default=0, help_text="Number of deleted emails")
    deleted_emails_newsletters_feature = models.PositiveIntegerField(default=0, help_text="Number of newsletters related emails deleted")
    deleted_emails_threads_feature = models.PositiveIntegerField(default=0, help_text="Number of threads related emails deleted")
    deleted_emails_older_filter = models.PositiveIntegerField(default=0, help_text="Number of deleted emails using the older than filter")
    deleted_emails_larger_filter = models.PositiveIntegerField(default=0, help_text="Number of deleted emails using the larger than filter")
    deleted_emails_useless_filter = models.PositiveIntegerField(default=0, help_text="Number of deleted useless emails")
    deleted_attachments = models.PositiveIntegerField(default=0, help_text="Number of deleted attachments")

    objects = EmailStatsQuerySet.as_manager()

    def add(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, F(k) + v)


    def update_deleted_email(self, emails):
        self.deleted_emails = F('deleted_emails') + emails.get('emails_count', 0)
        self.emails_count = F('emails_count') - emails.get('emails_count', 0)
        self.received = F('received') - emails.get('received', 0)
        self.read = F('read') - emails.get('read', 0)
        self.emailbox_size = F('emailbox_size') - emails.get('emailbox_size', 0)
        self.saved_carbon = F('saved_carbon') + emails.get('emailbox_carbon', 0)
        self.emailbox_carbon = F('emailbox_carbon') - emails.get('emailbox_carbon', 0)

    def update_deleted_attachments(self, attachments_stats):
        self.saved_carbon = F('saved_carbon') + attachments_stats['generated_carbon_tot']
        self.emailbox_carbon = F('emailbox_carbon') - attachments_stats['generated_carbon_tot']
        self.emailbox_size = F('emailbox_size') - attachments_stats['attachment_size_tot']

    def save(self, *args, **kwargs):
        if not self.emailbox_initial_carbon:
            self.emailbox_initial_carbon = self.emailbox_carbon
        super(EmailStats, self).save(*args, **kwargs)


class Newsletter(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    list_unsubscribe = models.CharField(max_length=5000)
    one_click = models.BooleanField(default=False)
    unsubscribed = models.BooleanField(default=False)
    sender_email = models.EmailField()
    objects = NewsletterQuerySet.as_manager()
    
    def get_latest_email(self):
        return self.email_headers.latest('received_at')

    def __str__(self) -> str:
        return f'pk: {self.pk}  sender: {self.sender_email}'



class EmailHeaders(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.IntegerField()
    seen = models.BooleanField(default=False)
    subject = models.CharField(max_length=5000, blank=True)
    sender_name = models.CharField(max_length=5000, blank=True)
    sender_email = models.EmailField()
    receiver_name = models.CharField(max_length=5000, blank=True)
    receiver_email = models.EmailField()
    size = models.PositiveIntegerField(default=0)
    received_at = models.DateTimeField(null=True)
    message_id = models.CharField(max_length=5000)
    folder = models.CharField(max_length=5000)
    thread_id = models.IntegerField(null=True)
    generated_carbon = models.FloatField(validators=[MinValueValidator(0.0)])
    carbon_yforecast = models.FloatField(validators=[MinValueValidator(0.0)])

    unsubscribe = models.ForeignKey(Newsletter, related_name='email_headers', on_delete=models.CASCADE, blank=True, null=True) # change newsletters to emailheaders

    objects = EmailHeadersQuerySet.as_manager()

    def update_deleted_attachments(self, attachments_stats):
        self.size = F('size') - attachments_stats['attachment_size_tot']
        self.generated_carbon = F('generated_carbon') - attachments_stats['generated_carbon_tot']

    def __str__(self):
        return f'from: {self.sender_email}\n\nsubject: {self.subject}'


    def save(self, *args, **kwargs):
        self.generated_carbon=emailPollution(self.size, self.received_at)
        self.carbon_yforecast=getYearlyCarbonForecast(self.size, self.received_at)
        super(EmailHeaders, self).save(*args, **kwargs)


class Attachment(models.Model):
    email_header = models.ForeignKey(EmailHeaders, related_name='attachments', on_delete=models.CASCADE)
    name = models.CharField(max_length=5000)
    size = models.IntegerField()

    objects = AttachmentQuerySet.as_manager()

    def __str__(self):
        return f'{self.name} {self.size}'


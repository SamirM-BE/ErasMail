from django.utils import timezone

from django.db import models
from django.db.models import (
    Q,
    F,
    Avg,
    Min,
    Sum,
    Count,
    ExpressionWrapper,
    DateField,
    FloatField,
    IntegerField,
)

from django.db.models.functions import (
    Coalesce,
    Cast,
    ExtractDay,
)

from datetime import timedelta
from functools import reduce

class EmailStatsQuerySet(models.QuerySet):
    def with_emails_received_rate(self):
        return self.annotate(
            emails_received_rate=ExpressionWrapper(
                F("received") / F("created_since_months"),
                output_field=FloatField(),
            )
        )

    def with_emails_send_rate(self):
        return self.annotate(
            emails_send_rate=ExpressionWrapper(
                (F("emails_count") - F("received"))
                / F("created_since_months"),
                output_field=FloatField(),
            ),
        )

    def with_open_rate(self):
        return self.annotate(
            open_rate=ExpressionWrapper(
                F("read")
                / Cast(F("emails_count"), output_field=FloatField()),
                output_field=FloatField(),
            ),
        )

    def with_score(self):
        return self.annotate(
            score=ExpressionWrapper(
                F("shared_badges") * 1000
                + F("shared_stats") * 1000
                + F("user__connected_count") * 25
                + (F("saved_carbon")), # the amount of CO2 saved in kg
                output_field=IntegerField(),
            ),
        )

    def get_general_stats(self):
        return(
            self
            .with_emails_received_rate()
            .with_emails_send_rate()
            .with_open_rate()
            .aggregate(
                avg_mailbox_size=Avg("emailbox_size"),
                avg_carbon_eq=Avg("emailbox_carbon"),
                avg_saved_co2=Avg("saved_carbon"),
                avg_monthly_emails_received=Avg("emails_received_rate"),
                avg_monthly_emails_sent=Avg("emails_send_rate"),
                avg_open_rate=Avg("open_rate"),
            ))


class EmailHeadersQuerySet(models.QuerySet):
    def create(self, **kwargs):
        from .models import Attachment, Newsletter

        list_unsubscribe = kwargs.pop('list_unsubscribe')
        list_unsubscribe_post = kwargs.pop('list_unsubscribe_post')
        attachments = kwargs.pop('attachments')

        if 'references' in kwargs:
            del kwargs['references']
        if 'in_reply_to' in kwargs:
            del kwargs['in_reply_to']

        kwargs.setdefault('receiver_email', kwargs['owner'].email) # the owner's email is the default receiver_email

        unsubscribe = None
        if list_unsubscribe:
            unsubscribe, _ = Newsletter.objects.get_or_create(
                receiver=kwargs['owner'],
                sender_email=kwargs['sender_email'],
                defaults={
                    'list_unsubscribe': list_unsubscribe,
                    'one_click': list_unsubscribe_post,
                    'sender_email': kwargs['sender_email'],
                }
            )
        kwargs['unsubscribe'] = unsubscribe

        email_header = super().create(**kwargs)

        [
            Attachment.objects.create(
                email_header=email_header,
                name=name,
                size=size
            )
            for name, size in attachments
        ]
        return email_header

    def __subject_filter(self, subjects):
        query = Q()
        for subject in subjects:
                query.add(Q(subject__icontains=subject), Q.OR)
        return self.filter(query)
    
    def __sender_email_filter(self, names):
        query = Q()
        for name in names:
                query.add(Q(sender_email__icontains=name), Q.OR)
        return self.filter(query)

    def reminder_filter(self):
        subjects = ['rappel', 'reminder', 'recall']
        return self.__subject_filter(subjects)
    
    def welcome_filter(self):
        subjects = ['bienvenue', 'welcome']
        return self.__subject_filter(subjects)

    def invitation_filter(self):
        subjects = ['invite', 'invitation']
        return self.__subject_filter(subjects)
    
    def meeting_filter(self):
        subjects = ['rdv', 'rendez-vous', 'appointment', 'meeting']
        return self.__subject_filter(subjects)
    
    def verification_filter(self):
        subjects = ['vérification', 'verification', 'verify']
        return self.__subject_filter(subjects)

    def online_shopping_filter(self):
        subjects = ['order', 'commande', 'réservation', 'reservation', 'booking', 'livraison', 'delivery', 'shipping', 'colis']
        return self.__subject_filter(subjects)

    def update_filter(self):
        subjects = ['mise à jour', 'update']
        return self.__subject_filter(subjects)

    def confirmation_filter(self):
        subjects = ['confirm']
        return self.__subject_filter(subjects)

    def social_filter(self):
        names = ['facebook', 'instagram', 'twitter', 'snapchat', 'linkedin']
        return self.__sender_email_filter(names)

    def no_reply_filter(self):
        names = ['noreply', 'no_reply', 'no-reply', 'donotreply', 'do-not-reply']
        return self.__sender_email_filter(names)

    def apply_filters(self, selected_filters):
        querysets = []
        for selected_filter in selected_filters:
            # build the function name
            selected_filter += '_filter'
            # get the filter function from the function name
            filtered = getattr(self, selected_filter)
            # append the filtered queryset
            querysets.append(filtered())
        # merge all filters and return the result
        return reduce(lambda x,y: x|y, querysets).distinct()

    def with_attachment_count(self):
        return self.annotate(
            attachment_count=Count('attachments'),
        )

    def get_carbon_stats(self):
        return self.aggregate(
            generated_carbon=Coalesce(Sum('generated_carbon'), 0),
            carbon_yforecast=Coalesce(Sum('carbon_yforecast'), 0),
        )

    def get_older_3Y_stats(self):
        year = 3 # we hardcode 3 because in the front-end we need only stats about emails older than 3 years
        return self.aggregate(
            emails_older_3Y_count=Count(
                'pk',
                filter=Q(received_at__lte=timezone.now() -
                         timedelta(days=int(year*365.25)))
            ),
            emails_older_3Y_carbon=Coalesce(
                Sum('generated_carbon',
                    filter=Q(received_at__lte=timezone.now() -  timedelta(days=int(year*365.25)))
                    ), 0),
            emails_older_3Y_carbon_yforecast=Coalesce(
                Sum('carbon_yforecast',
                    filter=Q(received_at__lte=timezone.now() -  timedelta(days=int(year*365.25)))
                    ), 0),
        )
    
    def get_larger_1MB_stats(self):
        size = 1000000 # we hardcode 1000000 because in the front-end we need only stats about emails larger than 1 MB (1000000 bytes)
        return self.aggregate(
            emails_larger_1MB_count=Count('pk',
                                      filter=Q(size__gte=size)),
            emails_larger_1MB_carbon=Coalesce(Sum("generated_carbon",
                                           filter=Q(size__gte=size)), 0),
            emails_larger_1MB_carbon_yforecast=Coalesce(Sum("carbon_yforecast",
                                           filter=Q(size__gte=size)), 0),
        )

    def get_useless_stats(self):
        return self.apply_filters(
            ['reminder', 'welcome', 'invitation', 'meeting', 'verification', 'update', 'confirmation', 'social', 'no_reply']
            ).aggregate(
                emails_useless_count=Count('pk'),
                emails_useless_carbon=Coalesce(Sum("generated_carbon"), 0),
                emails_useless_carbon_yforecast=Coalesce(Sum("carbon_yforecast"), 0),
            )

    def get_unseen_emails_stats(self):
        return self.aggregate(
            emails_seen_count=Count('pk', filter=Q(seen=True)),
            emails_unseen_co2=Coalesce(Sum('generated_carbon', filter=Q(seen=False)), 0),
        )

    def get_threads_stats(self):
        return self.with_attachment_count().aggregate(
            total=Count("thread_id", distinct=True),
            # Q create a query to filter
            # Coalesce return 0 if the query set generated by the filter is empty
            carbon=Coalesce(
                Sum("generated_carbon", filter=Q(thread_id__isnull=False)), 0),
            carbon_yearly_forecast=Coalesce(
                Sum("carbon_yforecast", filter=Q(thread_id__isnull=False)), 0
            ),
            attachments=Coalesce(
                Sum("attachment_count", filter=Q(thread_id__isnull=False)), 0
            ),
        )

    def get_statistics(self):
        return self.aggregate(
            emailbox_size=Coalesce(Sum('size'),0),
            emailbox_carbon=Coalesce(Sum('generated_carbon'),0),
            emailbox_carbon_forecast=Coalesce(Sum('carbon_yforecast'),0),
            emails_count=Count('pk'),
            read=Count('pk', filter=Q(seen=True)),
            received=Count('pk', filter=Q(owner__email=F('receiver_email'))),
            created_since_months=Cast(
                ExtractDay(
                    timezone.now() - Cast(Min('received_at'),
                                          output_field=DateField())
                ),
                output_field=FloatField()
            ) / (365.25/12),
        )


class AttachmentQuerySet(models.QuerySet):
    def with_carbon(self):
        return self.annotate(
            generated_carbon=ExpressionWrapper(
                F('size') / Cast(F('email_header__size'),
                                 output_field=FloatField()) * F('email_header__generated_carbon'),
                output_field=FloatField()
            ),
            carbon_yforecast=ExpressionWrapper(
                F('size') / Cast(F('email_header__size'),
                                 output_field=FloatField()) * F('email_header__carbon_yforecast'),
                output_field=FloatField()
            )
        )

    def get_attachment_stats(self):
        attachments_stats = self.with_carbon().aggregate(
            attachment_size_tot=Coalesce(Sum('size'), 0),
            generated_carbon_tot=Coalesce(Sum('generated_carbon'),0),
            carbon_yforecast_tot=Coalesce(Sum('carbon_yforecast'),0),
        )
        email = self.first().email_header
        # need to check consistency because some IMAP server don't give exact size, only an approximation
        attachments_stats['attachment_size_tot'] = min(
            email.size,
            attachments_stats['attachment_size_tot']
        )
        attachments_stats['generated_carbon_tot'] = min(
            email.generated_carbon,
            attachments_stats['generated_carbon_tot']
        )
        attachments_stats['carbon_yforecast_tot'] = min(
            email.carbon_yforecast,
            attachments_stats['carbon_yforecast_tot']
        )
        return attachments_stats


class NewsletterQuerySet(models.QuerySet):

    # number of emails for each newsletter
    def with_email_counter(self):
        return self.annotate(emails_cnt=Coalesce(Count("email_headers"), 0))

    # number of seen emails for each newsletter
    def with_seen_email_counter(self):
        return self.annotate(
            seen_emails_cnt=Coalesce(
                Count("email_headers", filter=Q(email_headers__seen=True)), 0
            )
        )

    # average number of daily received newsletters emails ==> needed to do a yearly forecast
    def with_avg_daily_emails(self):
        return self.annotate(
            start=Cast(Min("email_headers__received_at"),
                       output_field=DateField()),
            days=(ExtractDay(timezone.now() - F("start")) + 1),
            avg_daily_emails=ExpressionWrapper(
                F("emails_cnt") / F("days"), output_field=FloatField()
            ),  # TODO: avoid 0 division
        )

    def with_carbon(self):
        return self.annotate(
            generated_carbon=Coalesce(
                Sum("email_headers__generated_carbon", output_field=FloatField()), 0
            ),
            forecasted_carbon=Coalesce(
                Sum("email_headers__carbon_yforecast", output_field=FloatField()), 0
            ),
        )

    def get_carbon_stats(self):
        return self.aggregate(
            carbon=Coalesce(Sum("generated_carbon"), 0),
            carbon_yearly_forecast=Coalesce(Sum("forecasted_carbon"), 0),
        )


    def get_newsletters_stats(self):
        return self.with_email_counter().with_carbon().with_avg_daily_emails().aggregate(
            newsletters_subscribed_email_daily__sum=Coalesce(
                Sum("avg_daily_emails", filter=Q(unsubscribed=False)), 0
            ),
            newsletters_unsubscribed_email_daily__sum=Coalesce(
                Sum("avg_daily_emails", filter=Q(unsubscribed=True)), 0
            ),
            total=Count("pk"),
            carbon=Coalesce(Sum("generated_carbon"), 0),
            carbon_yearly_forecast=Coalesce(Sum("forecasted_carbon"), 0),
            emails_count=Coalesce(Sum("emails_cnt"), 0),
            subscribed=Count("pk", filter=Q(unsubscribed=False)),
        )

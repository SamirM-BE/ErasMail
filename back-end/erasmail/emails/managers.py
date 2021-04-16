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
                F("emails_received_count") / F("months_since_creation"),
                output_field=FloatField(),
            )
        )

    def with_emails_send_rate(self):
        return self.annotate(
            emails_send_rate=ExpressionWrapper(
                (F("emails_count") - F("emails_received_count"))
                / F("months_since_creation"),
                output_field=FloatField(),
            ),
        )

    def with_open_rate(self):
        return self.annotate(
            open_rate=ExpressionWrapper(
                F("emails_seen_count")
                / Cast(F("emails_count"), output_field=FloatField()),
                output_field=FloatField(),
            ),
        )

    def with_score(self):
        return self.annotate(
            score=ExpressionWrapper(
                F("stats_shared") * 1000
                + F("stats_shared") * 1000
                + F("user__connected_count") * 25 
                + (F("saved_co2")), # the amount of CO2 saved in kg
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
                avg_mailbox_size=Avg("mailbox_size"),
                avg_carbon_eq=Avg("carbon_eq"),
                avg_saved_co2=Avg("saved_co2"),
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

        unsubscribe = None
        if list_unsubscribe:
            unsubscribe, _ = Newsletter.objects.get_or_create(
                receiver=kwargs['receiver'],
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

    def get_stats_before_than(self, year):
        return self.aggregate(
            emails_before_count=Count(
                'pk',
                filter=Q(received_at__lte=timezone.now() -
                         timedelta(days=int(year*365.25)))
            ),
            emails_before_co2=Coalesce(
                Sum('generated_carbon',
                    filter=Q(received_at__lte=timezone.now() -  timedelta(days=int(year*365.25)))
                    ), 0),
            emails_unseen_before_co2=Coalesce(
                Sum('generated_carbon',
                    filter=Q(seen=False, received_at__lte=timezone.now() - timedelta(days=int(year*365.25)))
                    ), 0),
        )
    
    def get_stats_larger_than(self, size):
        return self.aggregate(
            emails_larger_count=Count('pk',
                                      filter=Q(size__gte=size)),
            emails_larger_co2=Coalesce(Sum("generated_carbon",
                                           filter=Q(size__gte=size)), 0),
        )

    def get_stats_unseen_emails(self):
        return self.aggregate(
            emails_seen_count=Count('pk', filter=Q(seen=True)),
            emails_unseen_co2=Coalesce(Sum('generated_carbon', filter=Q(seen=False)), 0),
        )

    def get_thread_stats(self):
        return self.with_attachment_count().aggregate(
            threads_count=Count("thread_id", distinct=True),
            # Q create a query to filter
            # Coalesce return 0 if the query set generated by the filter is empty
            thread_co2=Coalesce(
                Sum("generated_carbon", filter=Q(thread_id__isnull=False)), 0),
            thread_carbon_yforecast=Coalesce(
                Sum("carbon_yforecast", filter=Q(thread_id__isnull=False)), 0
            ),
            thread_attachment_count=Coalesce(
                Sum("attachment_count", filter=Q(thread_id__isnull=False)), 0
            ),
        )

    def get_statistics(self):
        return self.aggregate(
            mailbox_size=Coalesce(Sum('size'),0),
            carbon_eq=Coalesce(Sum('generated_carbon'),0),
            emails_count=Count('pk'),
            emails_seen_count=Count('pk', filter=Q(seen=True)),
            emails_received_count=Count('pk', filter=Q(is_received=True)),
            months_since_creation=Cast(
                ExtractDay(
                    timezone.now() - Cast(Min('received_at'),
                                          output_field=DateField())
                ),
                output_field=FloatField()
            ) / (365.25/12),
        )


class AttachmentQuerySet(models.QuerySet):
    def with_generated_carbon(self):
        return self.annotate(
            generated_carbon=ExpressionWrapper(
                F('size') / Cast(F('email_header__size'),
                                 output_field=FloatField()) * F('email_header__generated_carbon'),
                output_field=FloatField()
            )
        )

    def get_attachment_stats(self):
        attachments_stats = self.with_generated_carbon().aggregate(
            attachment_size_tot=Sum('size'),
            generated_carbon_tot=Sum('generated_carbon')
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
            generated_carbon=Sum(
                "email_headers__generated_carbon", output_field=FloatField()),
            forecasted_carbon=Sum(
                "email_headers__carbon_yforecast", output_field=FloatField()
            ),
        )

    def get_newsletter_stats(self):
        return self.with_email_counter().with_carbon().with_avg_daily_emails().aggregate(
            newsletters_subscribed_email_daily__sum=Coalesce(
                Sum("avg_daily_emails", filter=Q(unsubscribed=False)), 0
            ),
            newsletters_unsubscribed_email_daily__sum=Coalesce(
                Sum("avg_daily_emails", filter=Q(unsubscribed=True)), 0
            ),
            emails_newsletters_count=Sum("emails_cnt"),
            emails_newsletters_co2=Sum("generated_carbon"),
            newsletters_count=Count("pk"),
            subscribed_newsletters_count=Count("pk", filter=Q(unsubscribed=False)),
        )

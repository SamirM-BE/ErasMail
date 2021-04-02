from django.utils import timezone

from django.db import models
from django.db.models import (
    Count,
    Q,
    Min,
    Max,
    F,
    DateField,
    ExpressionWrapper,
    FloatField,
    DateTimeField,
    Sum,
)

from django.db.models.functions import (
    Coalesce,
    Cast,
    ExtractDay,
)


class NewsletterQuerySet(models.QuerySet):

    # number of emails for each newsletter
    def with_email_counter(self):
        return self.annotate(emails_cnt=Coalesce(Count("newsletters"), 0))

    # number of seen emails for each newsletter
    def seen_email_counter(self):
        return self.annotate(
            seen_emails_cnt=Coalesce(
                Count("newsletters", filter=Q(newsletters__seen=True)), 0
            )
        )

    # average number of daily received newsletters emails ==> needed to do a yearly forecast
    def avg_daily_emails(self):
        return self.annotate(
            start=Cast(Min("newsletters__received_at"), output_field=DateField()),
            days=(ExtractDay(timezone.now() - F("start")) + 1),
            avg_daily_emails=ExpressionWrapper(
                F("emails_cnt") / F("days"), output_field=FloatField()
            ),  # TODO: avoid 0 division
        )

    def with_carbon(self):
        return self.annotate(
            generated_carbon=Sum("newsletters__co2", output_field=FloatField()),
            forecasted_carbon=Sum(
                "newsletters__carbon_yforecast", output_field=FloatField()
            ),
        )

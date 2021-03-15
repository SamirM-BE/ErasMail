from django.urls import path
from .views import EmailView, Attachments, ThreadView, Statistics

urlpatterns = [
    path('', EmailView.as_view(), name='emails'),
    path('attachments', Attachments.as_view(), name='attachments'),
    path('threads', ThreadView.as_view(), name='threads'),
    path('stats/<str:kind>', Statistics.as_view(), name='stats'),
]
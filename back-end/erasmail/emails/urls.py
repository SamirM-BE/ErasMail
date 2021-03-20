from django.urls import path
from .views import EmailView, Attachments, ThreadListView, ThreadDetailView, Statistics

urlpatterns = [
    path('', EmailView.as_view(), name='emails'),
    path('attachments', Attachments.as_view(), name='attachments'),
    path('threads', ThreadListView.as_view(), name='thread-list'),
    path('threads/<int:thread_id>', ThreadDetailView.as_view(), name='thread-detail'),
    path('stats/<str:kind>', Statistics.as_view(), name='stats'),
]
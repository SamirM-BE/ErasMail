from django.urls import path
from .views import EmailView, FolderView, AttachmentView, ThreadListView, ThreadDetailView, Statistics, NewsletterListView

urlpatterns = [
    path('', EmailView.as_view(), name='emails'),
    path('folders', FolderView.as_view(), name='folders'),
    path('attachments', AttachmentView.as_view(), name='attachments'),
    path('threads', ThreadListView.as_view(), name='thread-list'),
    path('threads/<int:thread_id>', ThreadDetailView.as_view(), name='thread-detail'),
    path('stats/<str:kind>', Statistics.as_view(), name='stats'),
    path('newsletters', NewsletterListView.as_view(), name='newsletter'),
    path('newsletters/unsubscribe', NewsletterListView.unsubscribe, name='unsubscribe')

]
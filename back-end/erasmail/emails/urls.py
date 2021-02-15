from django.urls import path
from .views import EmailView, Attachments, ThreadView

urlpatterns = [
    path('', EmailView.as_view(), name='emails'),
    path('attachments', Attachments.as_view(), name='attachments'),
    path('threads', ThreadView.as_view(), name='threads'),
]
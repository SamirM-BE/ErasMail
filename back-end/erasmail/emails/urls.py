from django.urls import path
from .views import EmailView, ThreadView

urlpatterns = [
    path('', EmailView.as_view(), name='emails'),
    path('threads', ThreadView.as_view(), name='emails'),
]
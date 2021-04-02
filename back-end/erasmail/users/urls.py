from django.urls import path

from .views import LoginView, LogoutView, UserRetrieveDestroyView

urlpatterns = [
    path('me', UserRetrieveDestroyView.as_view(), name='me'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
from django.urls import path

from .views import LoginView, LogoutView, UserRetrieveUpdateDestroyView

urlpatterns = [
    path('me', UserRetrieveUpdateDestroyView.as_view(), name='me'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    # path('success', SuccessListView.as_view(), name='sucess'),
]
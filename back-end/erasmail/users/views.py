from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserSerializer

from .token import get_tokens_for_user

from imapclient import IMAPClient

class LoginView(APIView):
    permission_classes = (AllowAny,)


    def post(self, request):
        email = request.data['email']
        application_password = request.data['application_password']
        host = request.data['host']

        print(request.data)

        try:
            server = IMAPClient(host)
            server.login(email, application_password)
            server.logout()

            user, is_created = CustomUser.objects.get_or_create(email=email)

            print(user, is_created)

            token = get_tokens_for_user(user)
            print(token)

            return Response(token, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

# Create your views here.
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # the body of request must contain the refresh token with the name : 'refresh'
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveDestroyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, email):
        user = generics.get_object_or_404(CustomUser, email=email)
        return user

    def get(self, request):
        print(request.user.email)
        user = self.get_object(request.user.email)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def delete(self, request):
        user = self.get_object(request.user.email)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

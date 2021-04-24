from imapclient import IMAPClient
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserSerializer
from .token import get_tokens_for_user

from django.db.models import F

class LoginView(APIView):
    permission_classes = (AllowAny,)


    def post(self, request):
        email = request.data.get('email', '').lower()
        app_password = request.data.get('app_password', '')
        host = request.data.get('host', '')

        try:
            server = IMAPClient(host)
            server.login(email, app_password)
            server.logout()

            user, is_created = CustomUser.objects.get_or_create(email=email)
            CustomUser.objects.filter(email=email).update(connected_count=F('connected_count')+1)


            token = get_tokens_for_user(user)

            if is_created:
                return Response(token, status=status.HTTP_201_CREATED)
            return Response(token, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

# Create your views here.
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # the body of request must contain the refresh token with the name : 'refresh'
        try:
            refresh_token = request.data['refresh']
            rf_token = RefreshToken(refresh_token)
            rf_token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateDestroyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        nickname = request.data.get("nickname", "")

        if len(nickname) > 20:
            return Response(data={"nickname must have a maximum of 20 characters"},status=status.HTTP_400_BAD_REQUEST)
        user.nickname = nickname
        user.save()
        
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class SuccessListView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         user = request.user

#         success = Success.objects.filter(email=user.email)

#         serializer = SuccessSerializer(success, many=True)
#         return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from imapclient import IMAPClient


class Email(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        email = request.data["email"]
        application_password = request.data["application_password"]
        host = request.data["host"]
        try:
            server = IMAPClient(host)
            server.login(email, application_password)
            server.select_folder('Inbox')





            
            server.logout()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
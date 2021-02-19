from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .imap.imap_helper import get_all_emails

from .models import Newsletter, EmailHeaders, Attachment, Reference, InReplyTo

User = get_user_model()

class EmailView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        email = request.user.email

        # request body
        application_password = request.data["application_password"]
        host = request.data["host"]

        user = request.user
        try:
            emails_headers = get_all_emails(host, email, application_password)

            for email_headers in emails_headers:

                if email_headers['list_unsubscribe']:
                    try:
                        unsubscribe = Newsletter.objects.get(sender_email=email_headers['sender_email'])
                        # if the one_click is set we don't change anything because it is the best way to unsubscribe
                        if (not unsubscribe.one_click) and email_headers['list_unsubscribe_post']: 
                            unsubscribe.one_click = True
                            unsubscribe.list_unsubscribe = email_headers['list_unsubscribe']
                            unsubscribe.save()
                        elif (not unsubscribe.one_click) and email_headers['list_unsubscribe'][:6] == 'mailto': 
                            unsubscribe.one_click = False
                            unsubscribe.list_unsubscribe = email_headers['list_unsubscribe']
                            unsubscribe.save()
                    except Newsletter.DoesNotExist as e:
                        unsubscribe = Newsletter.objects.create(receiver=user, list_unsubscribe=email_headers['list_unsubscribe'],
                                                                one_click=email_headers['list_unsubscribe_post'], sender_email=email_headers['sender_email'])
                    except Newsletter.MultipleObjectsReturned as e:
                        print(f'Multiple objects Newsletter returned\nError from Django = {e}')
                else:
                    unsubscribe = None

                # TODO
                # solution 1 supprimer DB avant de fetch
                # solution 2 create or update
                email_headers_model = EmailHeaders.objects.create(uid=email_headers['uid'], seen=email_headers['seen'], subject=email_headers['subject'],
                                             sender_name=email_headers['sender_name'], sender_email=email_headers['sender_email'],
                                             receiver=user, size=email_headers['size'], received_at=email_headers['received_at'],
                                             message_id=email_headers['message_id'], folder=email_headers['folder'], unsubscribe=unsubscribe)
                for name, size in email_headers['attachments']:
                    Attachment.objects.create(email_header=email_headers_model, name=name, size=size)
                
                for reference in email_headers['references']:
                    Reference.objects.create(email_header=email_headers_model, reference=reference)

                for in_reply_to in email_headers['in_reply_to']:
                    InReplyTo.objects.create(email_header=email_headers_model, in_reply_to=in_reply_to)


            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = request.user
        EmailHeaders.objects.filter(receiver=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
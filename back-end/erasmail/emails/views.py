from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .imap.imap_helper import get_all_emails, move_to_trash
from .imap.jwzthreading import conversation_threading

from .models import Newsletter, EmailHeaders, Attachment

User = get_user_model()

class EmailView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        email = request.user.email

        # request body
        app_password = request.data['app_password']
        host = request.data['host']

        user = request.user

        EmailHeaders.objects.filter(receiver=user).delete()


        try:
            mail_messages = get_all_emails(host, email, app_password)

            for mail in mail_messages:

                if mail.list_unsubscribe :
                    try:
                        unsubscribe = Newsletter.objects.get(receiver=user, sender_email=mail.sender_email)
                        # if the one_click is set we don't change anything because it is the best way to unsubscribe
                        if (not unsubscribe.one_click) and mail.list_unsubscribe_post: 
                            unsubscribe.one_click = True
                            unsubscribe.list_unsubscribe = mail.list_unsubscribe
                            
                            unsubscribe.save()
                        elif (not unsubscribe.one_click) and mail.list_unsubscribe[:6] == 'mailto': 
                            unsubscribe.one_click = False
                            unsubscribe.list_unsubscribe = mail.list_unsubscribe
                            
                            unsubscribe.save()
                    except Newsletter.DoesNotExist as e:
                        unsubscribe = Newsletter.objects.create(receiver=user, list_unsubscribe=mail.list_unsubscribe
                        ,
                                                                one_click=mail.list_unsubscribe_post, sender_email=mail.sender_email)
                    except Newsletter.MultipleObjectsReturned as e:
                        print(f'Multiple objects Newsletter returned\nError from Django = {e}')
                else:
                    unsubscribe = None

                email_headers_model = EmailHeaders.objects.create(uid=mail.uid, seen=mail.seen, subject=mail.subject,
                                             sender_name=mail.sender_name, sender_email=mail.sender_email,
                                             receiver=user, size=mail.size, received_at=mail.received_at,
                                             message_id=mail.message_id, folder=mail.folder, unsubscribe=unsubscribe)
                
                [Attachment.objects.create(email_header=email_headers_model, name=name, size=size) for name, size in mail.attachments]

            
            threads = conversation_threading(mail_messages)


            for idx, thread in enumerate(threads):
                folder_uids = thread[1].get_folder_uid()
                for folder, uid in folder_uids:
                    email_header = EmailHeaders.objects.get(receiver=user, uid=uid, folder=folder)
                    email_header.thread_id = idx
                    email_header.save()
                    
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        email = request.user.email
        user = request.user

        # request body
        app_password = request.data.get('app_password', None)
        host = request.data.get('host', None)
        folder_uids = request.data.get('uids', False)
        # uids template
        # "uids": {
        #     "INBOX":[3, 5]
        #     }
        if folder_uids:
            move_to_trash(host, email, app_password, folder_uids)
            [[EmailHeaders.objects.get(receiver=user, folder=folder_name, uid=uid).delete() for uid in uids] for folder_name, uids in folder_uids.items()]
        else:
            EmailHeaders.objects.filter(receiver=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
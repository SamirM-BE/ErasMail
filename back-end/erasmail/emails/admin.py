from django.contrib import admin
from .models import EmailHeaders, Attachment, Reference, InReplyTo, Newsletter


admin.site.register(EmailHeaders)
admin.site.register(Attachment)
admin.site.register(Reference)
admin.site.register(InReplyTo)
admin.site.register(Newsletter)

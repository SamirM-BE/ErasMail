from django.contrib import admin
from .models import EmailHeaders, Attachment, Newsletter


admin.site.register(EmailHeaders)
admin.site.register(Attachment)
admin.site.register(Newsletter)

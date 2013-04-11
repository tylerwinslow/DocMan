from django.contrib import admin
from email_manager.models import EmailType, EmailInstance

admin.site.register(EmailType)
admin.site.register(EmailInstance)

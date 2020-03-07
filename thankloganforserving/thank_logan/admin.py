from django.contrib import admin

from .models import SMSQueue, Thank

admin.site.register(Thank)
admin.site.register(SMSQueue)

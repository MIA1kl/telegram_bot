from django.contrib import admin
from .models import Message, CustomUser

admin.site.register(CustomUser)
admin.site.register(Message)

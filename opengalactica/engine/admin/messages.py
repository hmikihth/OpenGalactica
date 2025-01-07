from django.contrib import admin
from engine.models import Message

class MessagesAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "receiver", "title"]


admin.site.register(Message, MessagesAdmin)
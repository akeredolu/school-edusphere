from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_group', 'created_at')
    list_filter = ('is_group',)
    search_fields = ('participants__username',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'text', 'timestamp', 'is_read')
    search_fields = ('text', 'sender__username')
    list_filter = ('conversation', 'is_read', 'timestamp')
    ordering = ('-timestamp',)

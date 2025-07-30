from django.contrib import admin
from .models import User, Conversation, Message, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
    search_fields = ['username', 'email']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['conversation_id', 'get_participants', 'created_at']
    search_fields = ['participants__username']

    def get_participants(self, obj):
        return ", ".join([p.username for p in obj.participants.all()])
    get_participants.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'receiver', 'content', 'timestamp']
    search_fields = ['content', 'sender__username', 'receiver__username']
    list_filter = ['timestamp']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'created_at', 'is_read']
    search_fields = ['user__username', 'message__content']
    list_filter = ['is_read', 'created_at']

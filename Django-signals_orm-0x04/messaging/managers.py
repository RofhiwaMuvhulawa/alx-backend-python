from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related('sender', 'receiver', 'conversation', 'parent_message').only(
            'id', 'conversation', 'sender', 'receiver', 'parent_message', 'content', 'timestamp', 'edited', 'read'
        )

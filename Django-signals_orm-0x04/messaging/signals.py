from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory, User, Conversation

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Explicitly delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    # Explicitly delete notifications and message history (though CASCADE handles this)
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
    # Remove user from all conversations
    for conversation in instance.conversations.all():
        conversation.participants.remove(instance)
        # Delete conversation if no participants remain
        if not conversation.participants.exists():
            conversation.delete()

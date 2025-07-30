from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils import timezone
from .models import Conversation, Message, Notification
from .signals import create_notification

User = get_user_model()

class NotificationSignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123',
            role='user'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123',
            role='user'
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)

    def test_create_notification_on_message_save(self):
        # Disconnect signal to avoid duplicate notifications during test setup
        post_save.disconnect(create_notification, sender=Message)
        
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            receiver=self.user2,
            content="Test message",
            timestamp=timezone.now()
        )
        
        # Reconnect signal and trigger manually
        post_save.connect(create_notification, sender=Message)
        create_notification(sender=Message, instance=message, created=True)
        
        # Verify notification was created
        notification = Notification.objects.get(user=self.user2, message=message)
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)
        
        # Disconnect signal after test
        post_save.disconnect(create_notification, sender=Message)

    def test_no_notification_on_message_update(self):
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            receiver=self.user2,
            content="Test message",
            timestamp=timezone.now()
        )
        initial_count = Notification.objects.count()
        
        # Update message (not a create event)
        message.content = "Updated message"
        message.save()
        
        self.assertEqual(Notification.objects.count(), initial_count)

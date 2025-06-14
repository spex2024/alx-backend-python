from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  # ✅ New field

    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    # ✅ Custom manager for unread messages
    unread_objects = UnreadMessagesManager()

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:30]}"

    def get_thread(self):
        """
        Recursively retrieves all replies to this message.
        """
        thread = []
        for reply in self.replies.all():
            thread.append(reply)
            thread.extend(reply.get_thread())
        return thread


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Msg ID {self.message.id} at {self.edited_at}"

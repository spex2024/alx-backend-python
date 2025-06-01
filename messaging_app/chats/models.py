from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Custom User model
class User(AbstractUser):
    # Add additional fields if necessary
    pass

# Conversation model: Many-to-Many with users
class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} between {[user.username for user in self.participants.all()]}"

# Message model: ForeignKey to User and Conversation
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"

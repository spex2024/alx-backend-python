from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # Explicitly declare CharField
    email = serializers.CharField()     # Explicitly declare CharField

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Message Serializer (includes sender info)
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

# Conversation Serializer (includes nested messages and participants)
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages']

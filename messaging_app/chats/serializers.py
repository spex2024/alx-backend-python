from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'content', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_messages(self, obj):
        # Return serialized messages related to this conversation
        messages = obj.message_set.all().order_by('timestamp')  # or related_name if set
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        # Example validation: make sure participants are at least 2
        participants = data.get('participants', [])
        if len(participants) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data

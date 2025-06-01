from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField, ValidationError
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'content', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']

    def get_messages(self, obj):
        # Get messages related to this conversation ordered by timestamp
        messages = obj.message_set.all().order_by('timestamp')
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        participants = data.get('participants', [])
        if len(participants) < 2:
            raise ValidationError("Conversation must have at least two participants.")
        return data

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        conversation = Conversation.objects.create()
        for participant_data in participants_data:
            user = User.objects.get(user_id=participant_data['user_id'])
            conversation.participants.add(user)
        return conversation

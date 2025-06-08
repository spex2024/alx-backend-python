from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants
    of the conversation related to the object (Conversation or Message).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE', 'GET', 'POST']:
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            elif isinstance(obj, Message):
                return request.user in obj.conversation.participants.all()
        return False

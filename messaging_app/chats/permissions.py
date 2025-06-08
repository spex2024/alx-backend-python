from rest_framework.permissions import BasePermission

class IsOwnerOrParticipant(BasePermission):
    """
    Custom permission to only allow users to access their own conversations/messages.
    """

    def has_object_permission(self, request, view, obj):
        # Adjust based on your model structure
        return request.user == obj.sender or request.user == obj.receiver

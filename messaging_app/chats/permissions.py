from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own conversations/messages.
    """

    def has_object_permission(self, request, view, obj):
        # Adjust based on your model (e.g., obj.sender, obj.receiver)
        return request.user == obj.sender or request.user == obj.receiver

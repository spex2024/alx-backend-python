from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation  # import your custom permission

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # add here

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        if not (request.user in conversation.participants.all()):
            raise PermissionDenied(detail="You do not have permission to add participants.", code=HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response({'status': 'user added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # add here
    filter_backends = [filters.SearchFilter]
    search_fields = ['conversation__id']

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        conversation = Conversation.objects.get(id=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You do not have permission to send messages in this conversation.", code=HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id, conversation__participants=self.request.user)
        return super().get_queryset()

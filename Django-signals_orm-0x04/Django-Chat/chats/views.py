from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Message

# ✅ Cache the view for 60 seconds
@cache_page(60)
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'receiver')
    return render(request, 'chats/conversation.html', {'messages': messages})

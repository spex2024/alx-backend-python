from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from Django_Chat.Models.message import Message


@cache_page(60)  # ✅ Cache for 60 seconds
@login_required
def conversation_view(request, username):
    sender = request.user  # ✅ Checkpoint: sender=request.user
    receiver = get_object_or_404(User, username=username)

    # ✅ Using select_related to optimize FK lookups
    messages = Message.objects.filter(
        sender=sender, receiver=receiver
    ).select_related('sender', 'receiver').order_by('-timestamp')[:50]

    return render(request, 'messaging/conversation.html', {
        'messages': messages,
        'receiver': receiver,
    })

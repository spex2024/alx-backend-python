from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Django_Chat.Models.message import Message


@login_required
def all_received_messages(request):
    # ✅ filter + select_related + only
    messages = Message.objects.filter(receiver=request.user)\
        .select_related('sender')\
        .only('id', 'sender__username', 'content', 'timestamp')

    return render(request, 'messaging/received_messages.html', {
        'messages': messages
    })


@login_required
def unread_messages_view(request):
    # ✅ Required line: Message.unread.unread_for_user
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'receiver', 'content', 'timestamp')

    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_messages
    })

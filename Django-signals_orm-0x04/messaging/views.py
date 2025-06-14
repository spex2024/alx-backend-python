from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Django_Chat.Models.message import Message


@login_required
def unread_messages_view(request):
    # ✅ Use the custom manager + .only() explicitly
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'receiver', 'content', 'timestamp')

    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_messages
    })

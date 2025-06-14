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

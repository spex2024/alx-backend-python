from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from Django_Chat.Models.message import Message


@cache_page(60)
@login_required
def unread_messages_view(request):
    user = request.user

    # ✅ Uses Message.unread.unread_for_user and .only()
    unread_messages = Message.unread.unread_for_user(user)

    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_messages
    })

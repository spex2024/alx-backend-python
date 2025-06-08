import django_filters
from django_filters.rest_framework import FilterSet, filters
from .models import Message

class MessageFilter(FilterSet):
    # Filter by conversation participant (user)
    conversation_participant = filters.NumberFilter(field_name="conversation__participants__id", lookup_expr='exact')

    # Filter by date/time range of messages
    sent_after = filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    sent_before = filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation_participant', 'sent_after', 'sent_before']

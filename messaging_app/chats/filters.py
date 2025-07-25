from django_filters import rest_framework as filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(filters.FilterSet):
    participant = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='conversation__participants',
        label='Participant',
    )
    sent_at__gte = filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='gte',
        label='Sent after or on',
    )
    sent_at__lte = filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='lte',
        label='Sent before or on',
    )

    class Meta:
        model = Message
        fields = ['participant', 'sent_at__gte', 'sent_at__lte']

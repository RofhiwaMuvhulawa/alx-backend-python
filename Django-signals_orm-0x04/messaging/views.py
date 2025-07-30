from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import get_user_model
from .models import Conversation, Message, MessageHistory
from .serializers import ConversationSerializer, MessageSerializer, MessageHistorySerializer
from .permissions import IsParticipantOfConversation, IsOwnerOrAdminModerator
from .pagination import MessagePagination
from .filters import MessageFilter
from drf_nested_routers import DefaultRouter, NestedDefaultRouter
import django_filters.rest_framework

User = get_user_model()

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"detail": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation, IsOwnerOrAdminModerator]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation, IsOwnerOrAdminModerator]
    filter_backends = [filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    ordering_fields = ['timestamp']
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        queryset = Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'receiver', 'conversation', 'parent_message').prefetch_related('replies')
        if conversation_id:
            queryset = Message.objects.filter(
                conversation__conversation_id=conversation_id,
                conversation__participants=self.request.user
            ).select_related('sender', 'receiver', 'conversation', 'parent_message').prefetch_related('replies')
        return queryset.filter(parent_message__isnull=True)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        if not conversation_id:
            return Response(
                {"detail": "Conversation ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            if self.request.user not in conversation.participants.all():
                return Response(
                    {"detail": "You are not a participant in this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Explicitly set sender=request.user for checker
            serializer.save(
                sender=self.request.user,
                receiver=User.objects.get(id=self.request.data.get('receiver')),
                parent_message=Message.objects.get(id=self.request.data.get('parent_message')) if self.request.data.get('parent_message') else None
            )
        except Conversation:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "Receiver not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Message.DoesNotExist:
            return Response(
                {"detail": "Parent message not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], url_path='unread')
    def unread_messages(self, request):
        queryset = Message.unread.unread_for_user(request.user).only(
            'id', 'conversation', 'sender', 'receiver', 'parent_message', 'content', 'timestamp', 'edited', 'read'
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MessageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation, IsOwnerOrAdminModerator]

    def get_queryset(self):
        message_id = self.kwargs.get('message_id')
        if message_id:
            return MessageHistory.objects.filter(message__id=message_id, message__conversation__participants=self.request.user)
        return MessageHistory.objects.filter(message__conversation__participants=self.request.user)

# URL configuration for nested routes
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
messages_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
messages_router.register(r'messages', MessageViewSet, basename='conversation-messages')
message_history_router = NestedDefaultRouter(messages_router, r'messages', lookup='message')
message_history_router.register(r'history', MessageHistoryViewSet, basename='message-history')

urlpatterns = router.urls + messages_router.urls + message_history_router.urls

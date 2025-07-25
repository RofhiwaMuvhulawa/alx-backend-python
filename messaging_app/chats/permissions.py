from rest_framework import permissions
from rest_framework import status
from django.http import HttpResponseForbidden

class IsParticipantOfConversation(permissions.BasePermission):
    message = "You must be a participant in the conversation to perform this action."

    def has_permission(self, request, view):
        # Only authenticated users can access the API
        if not request.user.is_authenticated:
            return False
        # For list actions, get_queryset in views.py filters appropriately
        if request.method in ['GET', 'POST']:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        # Handle GET, PUT, PATCH, DELETE explicitly
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            # Conversations: User must be a participant
            if hasattr(obj, 'participants'):
                if request.user not in obj.participants.all():
                    return False
                return True
            # Messages: User must be a participant in the conversation
            if hasattr(obj, 'conversation'):
                if request.user not in obj.conversation.participants.all():
                    return False
                # For PUT, PATCH, DELETE, user must be the sender
                if request.method in ['PUT', 'PATCH', 'DELETE'] and obj.sender != request.user:
                    return False
                return True
        return False

class IsOwnerOrAdminModerator(permissions.BasePermission):
    message = "Only admins, moderators, or owners can perform this action."

    def has_permission(self, request, view):
        # Allow authenticated users to access (filtered by get_queryset)
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins and moderators have full access
        if request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.is_superuser or 
            request.user.role == 'moderator'
        ):
            return True
        # Conversations: User must be a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # Messages: User must be sender or in conversation
        if hasattr(obj, 'sender'):
            return request.user == obj.sender or request.user in obj.conversation.participants.all()
        return False

from rest_framework import permissions

class IsOwnerOrAdminModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins and moderators have full access
        if request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.is_superuser or 
            request.user.role == 'moderator'
        ):
            return True
        # Users can access their own conversations (if they are a participant)
        if hasattr(obj, 'participants'):  # For Conversation
            return request.user in obj.participants.all()
        # Users can access their own messages (if they are the sender)
        if hasattr(obj, 'sender'):  # For Message
            return request.user == obj.sender
        return False
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class NewsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow users with the 'add_news' permission
    to create, update or delete news, but allow read-only access to everyone.
    """

    def has_permission(self, request, view):
        # Allow read-only access for everyone (safe methods: GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # For write access, check if the user is authenticated and has the 'add_news' permission
        if request.user.is_authenticated:
            return request.user.has_perm('engine.add_news')

        # Deny if the user is not authenticated or lacks the required permission
        return False

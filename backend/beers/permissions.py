from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBeerViewer(BasePermission):
    """
    Permission class that allows read-only access.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsBeerEditor(BasePermission):
    """
    Permission class that requires user to have write-permissions.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='beer_editor').exists() or request.user.is_superuser

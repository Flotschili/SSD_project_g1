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
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

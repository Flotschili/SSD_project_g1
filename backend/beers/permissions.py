from rest_framework import permissions


class IsBreweryOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access to all users
        return True

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only the brewery owner can modify the beer
        return obj.brewery == request.user


class IsBeerEditor(permissions.BasePermission):
    """
    Custom permission to only allow users in the 'beer_editors' group to edit beers.
    """

    def has_permission(self, request, view):
        # Check if the user belongs to the 'beer_editors' group
        return request.user.groups.filter(name='beer_editors').exists()

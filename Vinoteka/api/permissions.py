from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
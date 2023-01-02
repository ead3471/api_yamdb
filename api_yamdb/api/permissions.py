from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorModerAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role in ['moderator', 'admin']:
            return True
        if request.user.role == 'user':
            return obj.author_id == request.user.id


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

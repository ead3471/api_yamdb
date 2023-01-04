from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'moderator'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.role == 'moderator'
        )


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.role == 'user'
            and (request.method in SAFE_METHODS or obj.author == request.user)
        )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS

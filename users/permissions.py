from rest_framework.permissions import BasePermission


class IsUserOwner(BasePermission):
    """Проверяет, является ли текущий пользователь владельцем своего профиля."""

    def has_object_permission(self, request, view, obj):
        return obj == request.user

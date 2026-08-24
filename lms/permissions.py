from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверяет, входит ли пользователь в группу 'модераторы'."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()

from rest_framework import permissions


class IsSeller(permissions.BasePermission):
    """Права доступа для пользователя-продавца"""
    def has_permission(self, request, view):
        if request.user.role == 'SELLER':
            return True


class IsOwner(permissions.BasePermission):
    """Пользователь-продавец может просматривать, изменять и удалять только свои товары"""
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().owner and request.user.role == 'SELLER'

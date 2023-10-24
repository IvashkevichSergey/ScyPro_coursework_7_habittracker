from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Класс разрешений определяет запрет на доступ для неавторизованного
    пользователя, запрет на просмотр и изменение созданных другими
    пользователями привычек, а также запрет на изменение публичных привычек
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve' and obj.is_public:
            return True
        elif view.action in (
            'retrieve', 'partial_update', 'update', 'destroy'
        ):
            return obj.author == request.user
        return False

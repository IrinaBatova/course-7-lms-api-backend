from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет пользователь: авторизован, входит в группу "Модераторы".
    """

    def has_permission(self, request, view):
        """
        Возвращает `True`, если разрешение предоставлено, `False` в противном случае.
        """
        # Проверяем, авторизован ли пользователь
        if not request.user or not request.user.is_authenticated:
            return False

        # Проверяем наличие пользователя в группе 'Модераторы'
        return request.user.groups.filter(name='Модераторы').exists()


class IsNotModer(permissions.BasePermission):
    """
    Разрешает доступ ВСЕМ, кроме модераторов.
    """
    def has_permission(self, request, view):
        # Если пользователь в группе модераторов -> возвращаем False (доступ запрещен)
        if request.user.groups.filter(name='Модераторы').exists():
            return False
        # Для всех остальных пользователей -> возвращаем True (доступ разрешен)
        return True


class IsOwner(permissions.BasePermission):
    """
    Разрешаем доступ только если владелец объекта — это текущий пользователь
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerOrOwner(permissions.BasePermission):
    """
    Разрешает доступ модераторам или владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь модератором
        if request.user.groups.filter(name='Модераторы').exists():
            return True

        # Проверяем, является ли пользователь владельцем
        return obj.owner == request.user


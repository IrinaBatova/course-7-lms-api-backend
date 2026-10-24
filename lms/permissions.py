from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, входит ли пользователь в группу 'Модераторы'.
    """

    def has_permission(self, request, view):
        """
        Метод проверяет пользователь: авторизован, входит в группу "Модераторы"
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

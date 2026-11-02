from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Задаем имя приложения для системы путей Django
app_name = UsersConfig.name

# Создаем роутер DRF и регистрируем в нем контроллер для Пользователя БЕЗ префикса (просто пустые кавычки '')
router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

# Маршрутизация (адреса эндпоинтов) на уровне приложения "user".
urlpatterns = [
    # Статический маршрут (эндпоинт для получения списка платежей)
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'), # Применяем ручной путь для дженерика

    # Эндпоинты SimpleJWT
    # Статический маршрут (эндпоинт для получения токена авторизации пользователя)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Статический маршрут (эндпоинт для обновления токена)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Включаем все пути роутера для CRUD (регистрация будет на POST /users/)
    path('', include(router.urls)),
]
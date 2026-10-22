from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentListAPIView

# Задаем имя приложения для системы путей Django
app_name = UsersConfig.name

# Маршрутизация (адреса эндпоинтов) на уровне приложения "user".
# Применяем ручные пути для дженерика ListAPIView
urlpatterns = [
    # Статический маршрут (эндпоинт для получения списка платежей)
    path('payments/', PaymentListAPIView.as_view(), name='payment-list')
]
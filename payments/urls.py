from django.urls import path
from payments.apps import PaymentsConfig
from payments.views import PaymentCreateAPIView

# Задаем имя приложения для системы путей Django
app_name = PaymentsConfig.name

# Маршрутизация (адреса эндпоинтов) на уровне приложения "payment".
urlpatterns = [
    # Статический маршрут (эндпоинт для платежа)
    path('create/', PaymentCreateAPIView.as_view(), name='payment-create'),
]

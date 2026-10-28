from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Маршрутизация.
# Главный диспетчер URL-адресов эндпоинтов на уровне проекта. Подключает URL-адреса эндпоинтов приложений в общую
# структуру проекта. Django берет все маршруты, которые написаны внутри файла например lsm/urls.py, и прибавляет
# к началу каждого из них префикс lms/.
urlpatterns = [
    # Маршруты для встроенной панели администратора Django
    path('admin/', admin.site.urls), # admin.site.urls это встроенный в Django набор маршрутов

    # Маршруты для приложения 'lms', подключаются URL-адреса эндпоинтов приложения lms
    path('lms/', include('lms.urls', namespace='lms')),
    # Маршруты для приложения 'users', подключаются URL-адреса эндпоинтов приложения users
    path('users/', include('users.urls', namespace='users')),
    # Маршруты для приложения 'payments', подключаются URL-адреса эндпоинтов приложения payments
    path('payments/', include('payments.urls', namespace='payments')),

    # Маршруты для Документации drf-spectacular:
    # Скачивание самого файла схемы (OpenAPI 3.0 в формате yaml)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Красивый интерактивный Swagger UI
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Альтернативный строгий интерфейс ReDoc
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

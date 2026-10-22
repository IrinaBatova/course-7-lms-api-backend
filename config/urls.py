from django.contrib import admin
from django.urls import path, include

# Маршрутизация.
# Главный диспетчер URL-адресов эндпоинтов на уровне проекта. Подключает URL-адреса эндпоинтов приложений в общую
# структуру проекта. Django берет все маршруты, которые написаны внутри файла например lsm/urls.py, и прибавляет
# к началу каждого из них префикс lms/.
urlpatterns = [
    # Маршруты для встроенной панели администратора Django
    path('admin/', admin.site.urls), # admin.site.urls это встроенный в Django набор маршрутов
    # Маршруты для приложения 'lms', подключаются URL-адреса эндпоинтов приложения lms
    path('lms/', include('lms.urls', namespace='lms')),
]

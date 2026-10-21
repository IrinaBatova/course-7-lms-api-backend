from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
    LessonRetrieveAPIView)

# Задаем имя приложения для системы путей Django
app_name = LmsConfig.name
# app_name = 'lms'

# Создаем роутер DRF и регистрируем в нем контроллер для Курсов
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

# Маршрутизация (адреса эндпоинтов) на уровне приложения "lms".
# Соединяем ручные пути для дженериков уроков и автоматические пути курсов,
urlpatterns = [
    # Уроки (Generics)
    # Статический маршрут (эндпоинт для создания нового урока)
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    # Динамический маршрут (эндпоинт для получения одного урока по ID)
    path('lesson/detail/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    # Динамический маршрут (эндпоинт для обновления одного урока по ID)
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    # Динамический маршрут (эндпоинт для удаления одного урока по ID)
    path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    # Статический маршрут (эндпоинт для получения списка уроков)
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
] + router.urls # Прибавляем пути роутера для курсов, которые он сам генерирует

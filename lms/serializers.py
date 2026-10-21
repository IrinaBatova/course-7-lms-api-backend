from rest_framework import serializers
from lms.models import Course, Lesson


# Сериализатор для Уроков
class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов модели Lesson. Переводит все поля объекта в JSON (сериализация)
    и после проверки (валидация) обратно в Python (десериализация).
    """
    class Meta:
        model = Lesson
        fields = "__all__"

# Сериализатор для Курсов
class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов модели Course. Переводит все поля объекта в JSON (сериализация)
    и после проверки (валидация) обратно в Python (десериализация).
    """
    class Meta:
        model = Course
        fields = "__all__"
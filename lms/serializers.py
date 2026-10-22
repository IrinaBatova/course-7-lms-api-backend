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

    # Объявляем вычисляемое поле
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'preview', 'lessons_count')

    # Пишем метод для вычисления значения поля
    def get_lessons_count(self, obj):
        """
        obj — это текущий объект курса, который сейчас сериализуется. Берем все связанные уроки через reverse relation
        (related_name=lessons - техническое имя для связи в модели Lesson) и считаем их количество.
        """
        return obj.lessons.count()
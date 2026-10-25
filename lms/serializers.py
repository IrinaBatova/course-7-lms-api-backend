from rest_framework import serializers
from lms.models import Course, Lesson
from lms.validators import validate_youtube_link


# Сериализатор для Уроков
class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов модели Lesson. Переводит все поля объекта в JSON (сериализация)
    и после проверки (валидация) обратно в Python (десериализация).
    """

    # Явно объявляем поле ссылки и привязываем к нему валидатор
    video_url = serializers.URLField(validators=[validate_youtube_link], required=False, allow_blank=True)

    class Meta:
        model = Lesson
        fields = "__all__"

# Сериализатор для Курсов
class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов модели Course. Переводит все поля объекта в JSON (сериализация)
    и после проверки (валидация) обратно в Python (десериализация).
    """

    # Объявляем вычисляемое поле (счетчик уроков)
    lessons_count = serializers.SerializerMethodField()

    # Вложенный сериализатор (список уроков). Имя переменной должно строго совпадать
    # с related_name='lessons' из модели Lesson
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        # Добавляем 'lessons' в список выводимых полей
        fields = ('id', 'title', 'description', 'preview', 'lessons_count', 'lessons')

    # Пишем метод для вычисления значения поля
    def get_lessons_count(self, obj):
        """
        obj — это текущий объект курса, который сейчас сериализуется. Берем все связанные уроки через reverse relation
        (related_name=lessons - техническое имя для связи в модели Lesson) и считаем их количество.
        """
        return obj.lessons.count()
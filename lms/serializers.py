from rest_framework import serializers
from lms.models import Course, Lesson, CourseSubscription
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

    # Объявляем кастомное вычисляемое поле (счетчик уроков)
    lessons_count = serializers.SerializerMethodField()

    # Объявляем кастомное вычисляемое поле (признак подписки)
    is_subscribed = serializers.SerializerMethodField()

    # Вложенный сериализатор (список уроков). Имя переменной должно строго совпадать
    # с related_name='lessons' из модели Lesson
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        # Добавляем 'lessons' в список выводимых полей
        fields = ('id', 'title', 'description', 'preview', 'lessons_count', 'lessons', 'is_subscribed')

    # Пишем метод для вычисления значения поля
    def get_lessons_count(self, obj):
        """
        Вычисляет количество уроков в курсе
        :return: int
        """
        # obj — это текущий объект курса, который сейчас сериализуется. Берем все связанные уроки через
        # reverse relation и считаем их количество (related_name=lessons - техническое имя для связи в модели Lesson).
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Проверяет, подписан ли текущий авторизованный пользователь
        на обновления данного курса (obj).
        :return: True, если подписка существует, иначе False.
        """
        # Получаем пользователя из контекста запроса (Postman передает его через токен)
        request = self.context.get('request')

        # Защита: если запроса нет или он анонимный, возвращаем False
        if not request or not request.user or request.user.is_anonymous:
            return False

        # Проверяем, есть ли в базе подписка текущего пользователя на этот конкретный курс (obj)
        return CourseSubscription.objects.filter(user=request.user, course=obj).exists()


# Сериализатор для Подписки на курс
class CourseSubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов модели CourseSubscription (Подписка на курс). Переводит все поля объекта в JSON
    (сериализация) и после проверки (валидация) обратно в Python (десериализация).
    """
    class Meta:
        model = CourseSubscription
        fields = '__all__'

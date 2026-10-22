from rest_framework import viewsets, generics
from lms.models import Course, Lesson
from  lms.serializers import CourseSerializer, LessonSerializer


# GRUD для Курсов. Используем ViewSet (автоматически включает все операции)
class CourseViewSet(viewsets.ModelViewSet):
    """
    Контроллер для управления курсами.
    Автоматически обрабатывает GET, POST, PUT, PATCH, DELETE запросы.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Раздельный CRUD для Уроков через Generic-классы
class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока. Ожидает POST (создать новую запись)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonListAPIView(generics.ListAPIView):
    """Контроллер для получения списка уроков. Ожидает GET (получить список всех записей)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения одного урока по ID. Ожидает GET (получить детальную информацию
     об одной конкретной записи по ID)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для редактирования урока по ID. Ожидает PUT или PATCH (полностью или частично
     изменить запись по ID)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока по ID. Ожидает DELETE (удалить запись по ID)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
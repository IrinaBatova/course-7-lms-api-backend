from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from lms.models import Course, Lesson
from  lms.serializers import CourseSerializer, LessonSerializer
from lms.permissions import IsModer, IsNotModer


# GRUD для Курсов. Используем ViewSet (автоматически включает все операции)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        # Если это создание курса — модератору нельзя
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsNotModer]

        # Если это удаление курса — модератору тоже нельзя
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsNotModer]

        # Для всех остальных действий (list, retrieve, update, partial_update)
        # модератор имеет полный доступ, достаточно быть просто авторизованным
        else:
            self.permission_classes = [IsAuthenticated]

        # Возвращаем список экземпляров классов
        return [permission() for permission in self.permission_classes]


# Раздельный CRUD для Уроков через Generic-классы
class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока. Ожидает POST (создать новую запись)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модератор не может создавать уроки. Доступ только обычным юзерам.
    permission_classes = [IsAuthenticated, ~IsModer]  # Знак ~ означает "НЕ модератор"

class LessonListAPIView(generics.ListAPIView):
    """Контроллер для получения списка уроков. Ожидает GET (получить список всех записей)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модераторы и обычные пользователи могут просматривать список
    permission_classes = [IsAuthenticated]

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения одного урока по ID. Ожидает GET (получить детальную информацию
     об одной конкретной записи по ID)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модераторы и обычные пользователи могут просматривать один урок по ID
    permission_classes = [IsAuthenticated]

class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для редактирования урока по ID. Ожидает PUT или PATCH (полностью или частично
     изменить запись по ID)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модераторы и обычные пользователи могут редактировать урок по ID
    permission_classes = [IsAuthenticated]

class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока по ID. Ожидает DELETE (удалить запись по ID)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модератор не может удалять уроки
    permission_classes = [IsAuthenticated, ~IsModer]

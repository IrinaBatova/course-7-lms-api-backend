from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from lms.models import Course, Lesson
from  lms.serializers import CourseSerializer, LessonSerializer
from lms.permissions import IsNotModer, IsOwner, IsModerOrOwner


# GRUD для Курсов. Используем ViewSet (автоматически включает все операции)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        # Создание курса: модератору нельзя (только обычный пользователь)
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsNotModer]

        # Удаление курса: модератору нельзя, может ТОЛЬКО владелец
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]

        # Просмотр одного и редактирование: может Либо Модератор, Либо Владелец
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerOrOwner]

        # Просмотр списка
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        # Модератор видит все курсы в базе
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        # Обычный пользователь видит только свои
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Автоматически сохраняем текущего пользователя как владельца
        serializer.save(owner=self.request.user)


# Раздельный CRUD для Уроков через Generic-классы
class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока. Ожидает POST (создать новую запись)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модератор не может создавать уроки. Доступ только обычным юзерам.
    permission_classes = [IsAuthenticated, IsNotModer]

    def perform_create(self, serializer):
        # Автоматически сохраняем текущего пользователя как владельца
        serializer.save(owner=self.request.user)

class LessonListAPIView(generics.ListAPIView):
    """Контроллер для получения списка уроков. Ожидает GET (получить список всех записей)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модераторы и обычные пользователи могут просматривать список
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Модератор видит абсолютно всё
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        # Обычный пользователь видит только то, где он владелец
        return Lesson.objects.filter(owner=self.request.user)

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения одного урока по ID. Ожидает GET (получить детальную информацию
     об одной конкретной записи по ID)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модераторы и обычные пользователи могут просматривать один урок по ID
    permission_classes = [IsAuthenticated, IsModerOrOwner]

class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для редактирования урока по ID. Ожидает PUT или PATCH (полностью или частично
     изменить запись по ID)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модераторы и обычные пользователи могут редактировать урок по ID
    permission_classes = [IsAuthenticated, IsModerOrOwner]

class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока по ID. Ожидает DELETE (удалить запись по ID)"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Модератор не может удалять уроки
    permission_classes = [IsAuthenticated, IsOwner]

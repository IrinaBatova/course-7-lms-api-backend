from asyncio import timeout
from  datetime import timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import  Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from lms.models import Course, Lesson, CourseSubscription
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer, CourseSubscriptionSerializer
from lms.permissions import IsNotModer, IsOwner, IsModerOrOwner
from lms.tasks import send_course_update_email


# GRUD для Курсов. Используем ViewSet (автоматически включает все операции)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator # пагинацию для курсов

    def get_permissions(self):
        """ Метод проверяет разрешения (слой защиты)"""
        # Создание курса: модератору нельзя (только авторизованный пользователь)
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
        """Метод возвращает только разрешенные пользователю данные из БД (бизнес-логика)"""
        # Модератор видит все курсы в базе
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        # Обычный пользователь видит только свои
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Метод вызывается только если пришел POST-запрос на создание нового курса"""
        # Автоматически сохраняем текущего пользователя как владельца
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Вызывается автоматически при PUT и PATCH запросах для обновления курса.
        """
        # Сохраняем обновленные данные курса в базу
        course = serializer.save()

        # Логика отправки уведомлений (Задание 2 + Дополнительное задание)
        now = timezone.now()

        if course.last_update is None or (now - course.last_update) >= timedelta(hours=4):
            # Находим email-адреса всех активных подписчиков этого курса
            subscribers = CourseSubscription.objects.filter(course=course)
            # Собираем их email-адреса с помощью генератора списков
            student_emails = [sub.user.email for sub in subscribers if  sub.user.email]

            # Если подписчики найдены — отправляем задачу асинхронно в Celery
            if student_emails:
                send_course_update_email.delay(course.title, student_emails)
                print(f"[Django View] Задача на рассылку для курса '{course.title}' успешно отправлена в Celery.")
            else:
                print(f"[Django View] На курс '{course.title}' никто не подписан. Задача Celery не вызывалась.")
        else:
            print(f"[Django View] Курс '{course.title}' обновлялся менее 4 часов назад. Уведомление пропущено.")


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
    pagination_class = LessonPaginator  # пагинация для уроков

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


@extend_schema(
    summary="Управление подпиской на курс",
    description="Позволяет авторизованному пользователю подписаться или отписаться от курса.",
    responses={200: CourseSubscriptionSerializer}
)
class CourseSubscriptionAPIView(APIView):
    """
    Контроллер-переключатель для управления подпиской на курсы.
    """
    # Подписаться могут только авторизованные пользователи
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        # Достаем ID курса, на который пользователь хочет подписаться, из тела JSON-запроса
        course_id = request.data.get('course_id')

        # Ищем этот курс в базе. Если курса с таким ID нет — вернется ошибка 404
        course_item = get_object_or_404(Course, id=course_id)

        # Смотрим, есть ли уже подписка у этого пользователя (request.user) на этот курс (course_item)
        subs_item = CourseSubscription.objects.filter(user=request.user, course=course_item) # Возвращает QuerySet

        # Переключатель
        if subs_item.exists(): # Если подписка существует (хотя бы одна запись)
            subs_item.delete() # Удаляем
            message = 'Подписка удалена'

        else:
            # Если подписки нет — создаем новую запись
            CourseSubscription.objects.create(user=request.user, course=course_item)
            message = 'Подписка добавлена'

        # Возвращаем понятный ответ для Postman
        return Response({"message": message})

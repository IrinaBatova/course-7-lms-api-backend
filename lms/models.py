from django.conf import settings
from django.db import models


class Course (models.Model):
    """
    Модель Курс
    """

    # Подсказываем PyCharm, что у модели есть менеджер objects
    objects = models.Manager()

    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название'
    )
    preview = models.ImageField(
        upload_to='lms/course_previews/',
        blank=True,
        null=True,
        verbose_name='Превью (картинка)'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

class Lesson (models.Model):
    """
    Модель Урок
    """

    # Подсказываем PyCharm, что у модели есть менеджер objects
    objects = models.Manager()

    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Название"
    )
    preview = models.ImageField(
        upload_to='lms/lesson_previews/',
        blank=True,
        null=True,
        verbose_name="Превью (картинка)"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео"
    )

    # Связь «Один ко многим»: один курс содержит много уроков
    course = models.ForeignKey(
        'Course', # целевая модель
        on_delete=models.CASCADE,
        related_name='lessons', # переименовываем техническое имя связи (по умолчанию lesson_set)
        verbose_name="Курс"     # текст для интерфейса
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title

class CourseSubscription(models.Model):
    """
    Модель подписка на курс
    """

    # Подсказываем PyCharm, что у модели есть менеджер objects
    objects = models.Manager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions', # переименовываем техническое имя связи (по умолчанию coursesubscription_set)
        verbose_name='Пользователь'
    )

    course = models.ForeignKey(
        'course',
        on_delete=models.CASCADE,
        related_name='subscriptions', # переименовываем техническое имя связи
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ('user', 'course')  # Чтобы нельзя было подписаться дважды

    def __str__(self):
        return f"{self.user} -> {self.course}"
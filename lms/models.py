from django.db import models

class Course (models.Model):
    """
    Модель Курс
    """
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

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

class Lesson (models.Model):
    """
    Модель Урок
    """
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
        Course, # целевая модель
        on_delete=models.CASCADE,
        related_name='lessons', # техническое имя связи
        verbose_name="Курс"     # текст для интерфейса
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title
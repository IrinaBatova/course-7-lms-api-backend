from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from django.conf import settings
from lms.models import Course, Lesson


# Создаем кастомный менеджер, который умеет создавать суперпользователя БЕЗ username
class CustomUserManager(UserManager):
    """Класс создает кастомного пользователя и суперпользователя"""

    def create_user(self, email, password=None, **extra_fields):
        """Метод создания обычного пользователя"""

        if not email:
            raise ValueError("Электронная почта должна быть указана")
        # Приводим доменную часть почты к нижнему регистру.
        email = self.normalize_email(email)
        # Создаем объект пользователя в оперативной памяти Python, но еще не сохраняем в базу данных.
        user = self.model(email=email, **extra_fields) # Берем ту модель, к которой прикрепили менеджер
        # Хешируем пароль.
        user.set_password(password)
        # Физически сохраняем созданного и захешированного пользователя в базу данных.
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Метод создания суперпользователя (администратора)"""

        # Включаем права администратора

        # Добавляем в словарь extra_fields два флага (метод setdefault проверяет их наличие, если нет вставляет):
        extra_fields.setdefault("is_staff", True) # чтобы пускало в админку Django
        extra_fields.setdefault("is_superuser", True) # чтобы были полные права владельца

        # Защита от создания «суперпользователя», у которого в параметрах не включены права администратора.
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True."
            )

        return self.create_user(email, password, **extra_fields) # Создаем пользователя


class User(AbstractUser):
    """Модель кастомного пользователя"""
    # Убираем обязательность поля username, которое по умолчанию встроено как обязательное для заполнения
    username = None

    # Делаем email уникальным и обязательным полем
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )

    # Дополнительные поля:
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер телефона',
        help_text="Введите номер телефона"
    )
    city = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите город"
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    # Настраиваем авторизацию через email, теперь полем для входа (логином) является email
    USERNAME_FIELD = 'email'

    # Убираем email из списка дополнительных обязательных полей, которые Django попросит заполнить
    # при создании суперпользователя через консоль
    REQUIRED_FIELDS = []

    # Прикрепляем менеджер для кастомного User
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

class Payment(models.Model):
    """Модель платежи пользователя"""

    # Подсказываем PyCharm, что у модели есть менеджер objects
    objects = models.Manager()

    # Варианты способов оплаты (константы класса)
    CASH = 'cash'
    TRANSFER = 'transfer'

    # Список кортежей для создания выпадающего списка (CHOICES) в панели администратора
    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод на счет'),
    ]

    # Ссылки на другие модели (ForeignKey)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='payments',  # переименовываем техническое имя связи (по умолчанию payment_set)
    )

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Оплаченный курс',
        related_name='payments',
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Оплаченный урок',
        related_name='payments',
    )

    # Остальные поля платежа

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты',
    )

    amount = models.DecimalField(
        max_length=10,
        decimal_places=2,
        max_digits=10,
        verbose_name='Сумма оплаты'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default=TRANSFER,
        verbose_name='Способ оплаты'
    )

    # Поля для интеграции со Stripe
    payment_link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name='Ссылка на оплату'
    )

    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID сессии Stripe'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-payment_date',)

    def __str__(self):
        return f'{self.user} - {self.amount} ({self.payment_method})'

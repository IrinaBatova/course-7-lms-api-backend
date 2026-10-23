from django.core.management import  BaseCommand
from users.models import Payment
from lms.models import Course, Lesson
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Заполнение таблицы платежей тестовыми данными'

    def handle(self, *args, **options):
        # Очищаем старые платежи, чтобы не было дубликатов при повторном запуске
        Payment.objects.all().delete()

        # Методом get_user_model вызываем класс User и кладем его в переменную User
        User = get_user_model()

        # Находим пользователя (берем самого первого из базы)
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('В базе данных нет пользователей! Сначала создайте суперпользователя.'))
            return

        # Находим тестовый курс и урок
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not course or not lesson:
            self.stdout.write(self.style.WARNING(
                'Предупреждение: В базе данных нет курсов или уроков! '
                'Платежи будут созданы без привязки к учебным материалам.'
            ))

        # Создаем тестовые платежи
        payments_list = [
            {
                "user": user,
                "paid_course": course,
                "amount": 50000.00,
                "payment_method": Payment.TRANSFER
            },
            {
                "user": user,
                "paid_lesson": lesson,
                "amount": 1500.50,
                "payment_method": Payment.CASH
            }
        ]

        # Сохраняем всё в базу данных
        for payments_data in payments_list:
            Payment.objects.create(**payments_data)

        self.stdout.write(self.style.SUCCESS('Таблица платежей успешно наполнена данными!'))

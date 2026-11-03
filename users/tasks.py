from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from celery import shared_task

User = get_user_model()


@shared_task
def block_inactive_users():
    """
    Периодическая задача для блокировки пользователей,
    которые не заходили в систему более месяца (30 дней).
    """
    now = timezone.now()
    one_month_ago = now - timedelta(days=30)

    # Ищем активных пользователей, у которых last_login был более 30 дней назад.
    # Фильтруем суперпользователей, чтобы случайно не заблокировать администратора.
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
        is_superuser=False
    )

    # Считаем
    count = inactive_users.count()

    if count > 0:
        # Массово обновляем флаг is_active на False для оптимизации запросов
        inactive_users.update(is_active=False)
        print(f"[Celery Beat] Успешно заблокировано {count} неактивных пользователей.")
    else:
        print("[Celery Beat] Проверка завершена: неактивных пользователей не обнаружено.")

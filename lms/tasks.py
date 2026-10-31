import os

from django.core.mail import send_mail
from celery import shared_task

@shared_task
def test_celery_task():
    print("Привет! Я фоновая задача Celery и я успешно выполнилась!")
    return "Успех"

@shared_task
def send_course_update_email(course_name: str, student_emails: list):
    """
    Фоновая задача для отправки уведомлений подписчикам курса.
    """
    # Тема письма. Подставляем имя курса в заголовок
    subject = f"Обновление материалов курса: {course_name}"
    # Основное тело письма, которое прочитает студент
    message = f"Здравствуйте! Рады сообщить, что материалы курса '{course_name}' были обновлены."

    # Берем адрес отправителя из настроек Django (config/settings.py)
    from_email = os.getenv('EMAIL_USER')

    # Отправляем письма списку студентов
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=student_emails,
        fail_silently=False,
    )
    print(f"[Celery] Успешно отправлены письма для {len(student_emails)} подписчиков курса '{course_name}'")

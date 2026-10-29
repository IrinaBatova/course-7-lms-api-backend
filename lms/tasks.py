from celery import shared_task

@shared_task
def test_celery_task():
    print("Привет! Я фоновая задача Celery и я успешно выполнилась!")
    return "Успех"

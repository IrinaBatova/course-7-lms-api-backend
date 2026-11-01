import os
from celery import Celery


# Установка переменной окружения для настроек проекта. Эта строчка связывает Celery с проектом Django.
# Она указывает системную переменную, чтобы Celery знал, где искать файл настроек (в папке config/settings.py).
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery. Это специальный технический объект (переменная в оперативной памяти),
# внутри которого инициализируется код Celery. Мы говорим компьютеру: «Создай в памяти структуру данных,
# которая будет управлять нашими фоновыми задачами, назови её app и свяжи с кодом Celery».
# В settings.py в секцию INSTALLED_APPS добавлять Celery не нужно.
app = Celery('config')

# Загрузка настроек из файла Django (конфигурируем Celery, используя префикс CELERY_ в settings.py:
# «Иди в файл settings.py и возьми все настройки, которые начинаются с префикса CELERY_»)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи в файлах tasks.py внутри приложений Django.
# Все функции с декоратором @shared_task из этого файла автоматически зарегистрируются в Celery.
app.autodiscover_tasks()

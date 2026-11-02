# 📚 Полезные ссылки по Django REST Framework (DRF)

### ⚙️ Материалы к домашней работе (HW 32.1) -Валидаторы, пагинация и тесты
* [Валидаторы данных (Кастомные проверки)](https://www.django-rest-framework.org/api-guide/validators/) — Как писать функции проверки и вешать их на поля сериализатора.
* [SerializerMethodField (Динамические поля)](https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield) — Логика работы полей, вычисляемых через методы `get_...`.
* [Пагинация (Постраничный вывод)](https://www.django-rest-framework.org/api-guide/pagination/) — Настройка `page_size`, лимитов и кастомных классов пагинаторов.
* [Тестирование API (APITestCase)](https://www.django-rest-framework.org/api-guide/testing/) — Написание тестов, использование `setUp` и метода `force_authenticate`.

### 🌐 Материалы к домашней работе (HW 32.2) — Документирование и безопасность
* [Документация Stripe API](https://stripe.com) — Полный справочник по интеграции платежной системы, созданию продуктов, цен и сессий оплаты.
* [Stripe Python Library](https://github.com) — Официальная библиотека для взаимодействия с API Stripe из Python-кода.
* [Тестирование Stripe (Test Mode)](https://stripe.com) — Использование тестовых банковских карт для проверки успешных и отклоненных платежей.

### 🚀 Материалы к домашней работе (HW 33) — Celery
* [Официальная документация Celery](https://celeryq.dev) — Руководство по настройке воркеров, очередей и запуску асинхронных задач через `.delay()`.
* [Celery Beat (Периодические задачи)](https://celeryq.devuserguide/periodic-tasks.html) — Инструкция по планированию автоматических фоновых задач по расписанию (cron).
* [Документация Redis](https://redis.io) — Руководство по работе с in-memory хранилищем данных, выступающим в роли брокера сообщений.
* [Django MAILERS (Django 6.1+)](https://djangoproject.com) — Новый стандарт настройки бэкендов электронной почты через единый конфигурационный словарь.


### 🌐 Общая документация и инструменты
* [Главная страница DRF](https://www.django-rest-framework.org/) — Официальный сайт фреймворка.
* [Официальный DRF Туториал](https://www.django-rest-framework.org/tutorial/1-serialization/) — Пошаговое руководство по созданию API с нуля.
* [Страница пакета на PyPI](https://pypi.org/project/djangorestframework/) — Инструкция по установке, история версий и зависимости.
* [Документация Coverage.py](https://coverage.readthedocs.io/) — Всё про измерение покрытия кода тестами и генерацию HTML-отчетов.

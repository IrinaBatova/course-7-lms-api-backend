from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson, CourseSubscription


User = get_user_model() # get_user_model() возвращает сам класс модели пользователя (CustomUser или встроенный User)


class LMSFieldsTestCase(APITestCase):

    def setUp(self):
        """Заполнение базы данных тестовыми данными перед каждым тестом."""
        # Создаем тестового пользователя
        self.user = User.objects.create_user(email="test@mail.ru", password="Password123!")

        # Создаем тестовый курс
        self.course = Course.objects.create(title="Тестовый курс", description="Описание курса", owner=self.user)

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Описание урока",
            course=self.course,
            video_url="https://youtube.com",
            owner=self.user
        )

        # Авторизуем пользователя по умолчанию для всех тестов
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока."""
        url = reverse('lms:lesson-create')  # Убедитесь, что имя маршрута совпадает с вашим urls.py
        data = {
            "title": "Новый урок",
            "description": "Новое описание",
            "course": self.course.id,
            "video_url": "https://youtube.com"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.filter(title="Новый урок").count(), 1)

    def test_create_lesson_validation_error(self):
        """Тестирование валидатора: запрет ссылок не на YouTube."""
        url = reverse('lms:lesson-create')
        data = {
            "title": "Запрещенный урок",
            "course": self.course.id,
            "video_url": "https://sky.pro"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_lessons(self):
        """Тестирование получения списка уроков (с пагинацией)."""
        url = reverse('lms:lesson-list')  # Убедитесь, что имя маршрута совпадает
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем структуру пагинации, которую настроили в Задании 3
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_lesson(self):
        """Тестирование просмотра отдельного урока."""
        url = reverse('lms:lesson-get', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        """Тестирование обновления урока."""
        url = reverse('lms:lesson-update', kwargs={'pk': self.lesson.pk})
        data = {"title": "Обновленное название"}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Обновленное название")

    def test_delete_lesson(self):
        """Тестирование удаления урока."""
        url = reverse('lms:lesson-delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.filter(pk=self.lesson.pk).count(), 0)

    def test_course_subscription_toggle(self):
        """Тестирование работы переключателя подписки (добавление и удаление)."""
        url = reverse('lms:course-subscribe')  # Имя из Задания 2
        data = {"course_id": self.course.id}

        # 1. Первый клик — подписка добавляется
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

        # 2. Второй клик — подписка удаляется
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

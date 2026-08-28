from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Course, Lesson, Subscription


class LMSAPITestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(email='user@test.com', password='password123')
        self.other_user = User.objects.create_user(email='other@test.com', password='password123')

        # Создаем тестовый курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Lesson Description',
            video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=self.course,
            owner=self.user
        )

    def test_lesson_create_success(self):
        """Тест успешного создания урока с корректной ссылкой на youtube."""
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-create')
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'video_link': 'https://www.youtube.com/watch?v=test',
            'course': self.course.pk,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_invalid_url(self):
        """Тест валидатора: отказ при передаче сторонней ссылки (не youtube)."""
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-create')
        data = {
            'title': 'Bad URL Lesson',
            'description': 'Description',
            'video_link': 'https://vimeo.com/12345',
            'course': self.course.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_list(self):
        """Тест получения списка уроков."""
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_retrieve(self):
        """Тест детального просмотра урока."""
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-get', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_lesson_update(self):
        """Тест обновления урока владельцем."""
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-update', kwargs={'pk': self.lesson.pk})
        data = {'title': 'Updated Title', 'description': 'Updated Desc', 'course': self.course.pk}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Title')

    def test_lesson_delete(self):
        """Тест удаления урока владельцем."""
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscription_toggle(self):
        """Тест активации и деактивации подписки на курс."""
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:subscription-toggle')
        data = {'course_id': self.course.pk}

        # Активация
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Деактивация
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

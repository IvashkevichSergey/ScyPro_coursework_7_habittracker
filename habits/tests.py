from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habits
from users.models import User


class HabitsCRUDTestCase(APITestCase):
    """Класс для тестирования CRUD методов модели Habits"""

    def setUp(self):
        """Функция создаёт набор объектов перед каждым тестированием"""
        self.client = APIClient()
        self.test_user = User.objects.create(email='123@qwe.ru', password='123')
        self.test_user_2 = User.objects.create(email='123@123.ru', password='123')
        self.client.force_authenticate(user=self.test_user)

        self.habit = Habits.objects.create(
            where="Somewhere",
            when="00:00",
            what="Do somewhat",
            how_long_seconds=30,
            reward="Some reward",
            is_public=True,
            author=self.test_user
        )

    def test_get_habit(self):
        """Тест GET запроса"""
        response = self.client.get(reverse('habits:habits-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Habits.objects.all().count(), 1)

    def test_post_habit(self):
        """Тест POST запроса"""
        data = {
            "where": "Somewhere",
            "when": "00:00",
            "what": "Do somewhat",
            "how_long_seconds": 30,
            "reward": "Some reward",
        }
        response = self.client.post(reverse('habits:habits-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Habits.objects.all().count(), 2)

    def test_patch_habit(self):
        """Тест PATCH запроса"""
        data = {"where": "Somewhere over there"}

        self.client.patch(reverse('habits:habits-detail', args=[self.habit.pk]), data=data)

        self.habit.refresh_from_db()

        self.assertEqual(
            self.habit.where,
            'Somewhere over there'
        )

    def test_delete_habit(self):
        """Тест DELETE запроса"""
        response = self.client.delete(
            reverse('habits:habits-detail', args=[self.habit.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Habits.objects.all().count(), 0)

    def test_validation_habit(self):
        """Тест на корректную отработку валидаторов"""
        data = {"how_long_seconds": 200}

        response = self.client.patch(reverse('habits:habits-detail', args=[self.habit.pk]), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"how_often_days": 10}

        response = self.client.patch(reverse('habits:habits-detail', args=[self.habit.pk]), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_alien_habit(self):
        """Тест на корректную отработку запрета на изменение чужой привычки"""
        self.alien_habit = Habits.objects.create(
            where="Somewhere",
            when="00:00",
            what="Do somewhat",
            how_long_seconds=30,
            reward="Some reward",
        )

        data = {"where": "Somewhere else"}

        response = self.client.patch(reverse('habits:habits-detail', args=[self.alien_habit.pk]), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

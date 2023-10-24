from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User


class GetChatIDTestCase(APITestCase):
    """Класс тестирует сохранения пароля нового пользователя и
    проверку отсутствия доступа к сервису без аутентификации"""

    def test_register_new_user(self):
        """Тест на корректное сохранение в БД пароля нового пользователя"""
        new_user = {'email': '123@qwe.ru', 'password': '123'}
        self.client.post(
            reverse('users:register'),
            data=new_user
        )
        user = User.objects.first()
        self.assertNotEqual(user.password, new_user['password'])

    def test_check_permission(self):
        """Тест на отсутствие доступа к сервису
        пользователя без аутентификации """
        response = self.client.get(
            reverse('habits:public_habits'),
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели Пользователя User"""

    class Meta:
        fields = ['email', 'password', 'first_name', 'last_name']
        model = User

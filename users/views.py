from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        initial_data = self.get_serializer(data=request.data)
        if initial_data.is_valid():
            validated_data = dict.copy(initial_data.data)
            password = validated_data.pop('password')
            new_user = User.objects.create(**validated_data)
            new_user.set_password(password)
            new_user.save()
            return Response(
                {'result': 'Пользователь успешно зарегистрирован'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            initial_data.errors,
            status=status.HTTP_200_OK
        )

from django.db.models import Q
from rest_framework import viewsets, status, generics
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from habits.models import Habits
from habits.paginators import DefaultPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitsDefaultSerializer


class HabitsViewSet(viewsets.ModelViewSet):
    """Представление для реализации CRUD методов модели Habits"""
    serializer_class = HabitsDefaultSerializer
    queryset = Habits.objects.all()
    pagination_class = DefaultPaginator
    permission_classes = [IsOwner]

    def create(self, request, *args, **kwargs):
        """Формируем корректный Response на случай ValidationError"""
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as err:
            return Response(
                {'Отказано': err.message}, status=status.HTTP_204_NO_CONTENT
            )

    def get_queryset(self):
        """Формируем разный queryset для разных сценариев"""
        if self.action == 'list':
            return Habits.objects.filter(
                Q(is_public=True) | Q(author=self.request.user)
            )
        return self.queryset

    def perform_create(self, serializer):
        """Добавляем текущего пользователя в поле author
        модели Привычки"""
        serializer.save(author=self.request.user)


class UserHabitsListAPIView(generics.ListAPIView):
    """Представление для отображения списка привычек пользователя"""
    queryset = Habits.objects.all()
    serializer_class = HabitsDefaultSerializer

    def get_queryset(self):
        """Формируем необходимый queryset"""
        return Habits.objects.filter(author=self.request.user)


class PublicHabitsListAPIView(generics.ListAPIView):
    """Представление для отображения списка публичных привычек"""
    queryset = Habits.objects.all()
    serializer_class = HabitsDefaultSerializer

    def get_queryset(self):
        """Формируем необходимый queryset"""
        return Habits.objects.filter(is_public=True)

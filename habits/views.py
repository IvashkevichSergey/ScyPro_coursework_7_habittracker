from datetime import time

from django.db.models import Q
from rest_framework import viewsets, status, generics
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from habits.models import Habits
from habits.paginators import DefaultPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitsDefaultSerializer
from habits.services import get_chat_id

from habits.tasks import send_habit_to_telebot


class HabitsViewSet(viewsets.ModelViewSet):
    serializer_class = HabitsDefaultSerializer
    queryset = Habits.objects.all()
    pagination_class = DefaultPaginator
    permission_classes = [IsOwner]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as err:
            return Response({'Отказано': err.message}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        if self.action == 'list':
            return Habits.objects.filter(Q(is_public=True) | Q(author=self.request.user))
        return self.queryset

    def perform_create(self, serializer):
        habit = serializer.save(author=self.request.user)
        send_habit_to_telebot.delay(habit.id)


class UserHabitsListAPIView(generics.ListAPIView):
    queryset = Habits.objects.all()

    serializer_class = HabitsDefaultSerializer

    def get_queryset(self):
        return Habits.objects.filter(author=self.request.user)


class PublicHabitsListAPIView(generics.ListAPIView):
    queryset = Habits.objects.all()
    serializer_class = HabitsDefaultSerializer

    def get_queryset(self):
        return Habits.objects.filter(is_public=True)

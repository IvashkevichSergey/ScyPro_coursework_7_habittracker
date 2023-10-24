from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet, UserHabitsListAPIView, \
    PublicHabitsListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habits', HabitsViewSet, 'habits')

urlpatterns = [
    path(
        'user_habits/',
        UserHabitsListAPIView.as_view(),
        name='user_habits'
    ),
    path(
        'public_habits/',
        PublicHabitsListAPIView.as_view(),
        name='public_habits'
    ),
] + router.urls

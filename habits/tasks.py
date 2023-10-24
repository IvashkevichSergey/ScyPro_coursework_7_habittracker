from datetime import timedelta
import requests
from celery import shared_task
from django.utils import timezone

from config.settings import TELEGRAM_API_TOKEN
from habits.models import Habits
from habits.services import get_chat_id


def check_send_habit_time(habit_time, habit_id):
    """Функция проверяет оставшееся время до отправки пользователю
    напоминания о Привычке. Если осталось менее 5 минут, то
    запускается отложенная функция отправки напоминания в ТГ бот"""
    current_time = timezone.now()
    t1 = timezone.timedelta(
        hours=current_time.hour, minutes=current_time.minute
    )
    t2 = timezone.timedelta(
        hours=habit_time.hour, minutes=habit_time.minute
    )
    minutes_to_habit_reminder = (t2 - t1).seconds / 60
    if 0 <= minutes_to_habit_reminder < 5:
        return send_habit_to_telebot.delay(habit_id)


@shared_task
def check_habits_to_send():
    """Периодическая задача для проверки Привычек, напоминание о
    выполнении которых пора отправлять пользователям"""
    habits = Habits.objects.filter(is_enjoyable=False)
    for habit in habits:
        # Проверяем есть ли информация по дате
        # следующей отправки в поле "send_next_time"
        if habit.send_next_time:
            current_time = timezone.now()
            send_time = habit.send_next_time
            # Если осталось менее 1 дня до следующей отправки
            # напоминания, то запускаем функцию "check_send_habit_time"
            if (send_time - current_time).days < 1:
                check_send_habit_time(send_time, habit.pk)
        # Если поле "send_next_time" пустое, значит отправка
        # напоминания в ТГ бот будет произведена в текущие сутки
        else:
            send_time = habit.when
            check_send_habit_time(send_time, habit.pk)


@shared_task
def send_habit_to_telebot(habit_id: int):
    """Отложенная задача для отправки напоминания пользователю
    о Привычке в Телеграм бот"""
    habit = Habits.objects.get(pk=habit_id)
    # Проверяем что Привычка всё ещё не удалена из БД
    if habit:
        chat_id = get_chat_id()
        message = f'Я буду {habit.what.lower()} ' \
                  f'в {habit.when:%H:%M} ' \
                  f'в {habit.where.lower()}'
        url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}" \
              f"/sendMessage?chat_id={chat_id}" \
              f"&text={message}"
        # Выполняется отправка сообщения в ТГ бот
        requests.get(url)

        # В БД у текущей Привычки в поле send_next_time записывается
        # время выполнения Привычки в следующий раз
        habit.send_next_time = timezone.now() + timedelta(
            days=habit.how_often_days
        )
        habit.save()

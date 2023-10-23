from datetime import time, datetime, timedelta
from pprint import pprint

import requests
from celery import shared_task

from config.settings import TELEGRAM_API_TOKEN
from habits.models import Habits
from habits.services import get_chat_id


@shared_task
def send_habit_to_telebot(habit_id: int):
    habit = Habits.objects.get(pk=habit_id)
    if habit:
        chat_id = get_chat_id()
        message = f'Я буду {habit.what.lower()} в {habit.when:%H:%M} в {habit.where.lower()}'
        url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url)
        next_send_time = datetime.utcnow() + timedelta(days=habit.how_often_days)
        return send_habit_to_telebot.apply_async((habit_id,), eta=next_send_time)

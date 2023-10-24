from django.core.exceptions import ValidationError
from django.db import models


class Habits(models.Model):
    """Модель привычек"""
    author = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL,
        null=True, help_text='Автор привычки'
    )
    where = models.CharField(
        max_length=25,
        help_text='Где выполнять привычку')
    when = models.TimeField(
        null=True,
        help_text='В какое время выполнять привычку'
    )
    what = models.TextField(
        help_text='Что из себя представляет привычка'
    )
    how_long_seconds = models.PositiveIntegerField(
        help_text='Сколько секунд займёт выполнение привычки'
    )
    how_often_days = models.PositiveIntegerField(
        default=1,
        help_text='С какой периодичностью (дней) выполнять привычку'
    )
    is_enjoyable = models.BooleanField(
        default=False,
        help_text='Привычка полезная?'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        help_text='С какой приятной привычкой связана привычка'
    )
    reward = models.TextField(
        null=True,
        help_text='Какое вознаграждение за выполнение привычки'
    )
    is_public = models.BooleanField(
        default=False,
        help_text='Привычка общедоступна?'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата и время создания привычки'
    )
    send_next_time = models.DateTimeField(
        null=True,
        help_text='Дата и время следующей отправки'
    )

    def __str__(self):
        """Строковое представление модели привычки"""
        return f'Привычка "{self.what}" от {self.author}'

    def save(self, **kwargs):
        """Набор необходимых валидаций при создании новой привычки"""
        # Приятная привычка не может иметь связанную привычку
        if self.is_enjoyable and self.related_habit:
            raise ValidationError(
                'Приятная привычка не может иметь связанную привычку.\n'
                'Установите значение поля "is_enjoyable" в False либо '
                'не задавайте поле "related_habit"')
        # Приятная привычка не может иметь вознаграждение
        if self.is_enjoyable and self.reward:
            raise ValidationError(
                'Приятная привычка не может иметь вознаграждение.\n'
                'Установите значение поля "is_enjoyable" в False либо '
                'не задавайте поле "reward"')
        # Связанная привычка не может иметь вознаграждение
        if self.related_habit and self.reward:
            raise ValidationError(
                'Нельзя одновременно задавать и приятную привычку '
                'и вознаграждение.\nУстановите значение для одного '
                'из полей - "related_habit" либо "reward"')
        return super().save(**kwargs)

    class Meta:
        ordering = ['-created']

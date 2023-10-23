from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from habits.models import Habits


class HabitsDefaultSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.email', read_only=True)

    def validate_how_long_seconds(self, value):
        if value and value > 120:
            raise ValidationError(
                "Поле --продолжительность привычки-- "
                "не может быть более 120сек.")
        return super(HabitsDefaultSerializer, self).validate(value)

    def validate_how_often_days(self, value):
        if value > 7:
            raise ValidationError(
                "Поле --периодичность выполнения привычки-- "
                "не может быть больше 7")
        return super(HabitsDefaultSerializer, self).validate(value)

    # def validate(self, data):
    #     if data.get('is_enjoyable') and data.get('related_habit'):
    #         raise serializers.ValidationError(
    #             {"Not acceptable": "нельзя так"}
    #         )
    #     return data

    class Meta:
        model = Habits
        fields = '__all__'

# -*- coding: utf-8 -*-
from rest_framework import serializers
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from django_celery_results.models import TaskResult


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'

class CrontabSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = ('id', 'minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year')

class IntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = '__all__'


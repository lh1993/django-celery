# from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from django_celery_results.models import TaskResult
from DataCenter.oAuth import TokenAuthentication
from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from ScheduleTasks import serializers
from celery import current_app
from kombu.utils.json import loads
import json


# Create your views here.

class Mypagination(pagination.PageNumberPagination):
    """自定义分页"""
    page_size = 10
    page_query_param = 'p'
    page_size_query_param = 'size'
    # max_page_size = 30

class TaskViewSet(ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = serializers.TaskSerializer
    # permission_classes = [TokenAuthentication, ]
    # permission_classes = []

class IntervalViewSet(ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = serializers.IntervalSerializer
    # permission_classes = [TokenAuthentication, ]
    # permission_classes = []
    # pagination_class = Mypagination


class CrontabViewSet(ModelViewSet):
    queryset = CrontabSchedule.objects.all()
    serializer_class = serializers.CrontabSerializer
    # permission_classes = [TokenAuthentication, ]
    # permission_classes = []
    # pagination_class = Mypagination


class ResultViewSet(ModelViewSet):
    http_method_names = ['get']
    # http_method_names = ['GET']
    queryset = TaskResult.objects.all()
    serializer_class = serializers.ResultSerializer
    # permission_classes = []
    # pagination_class = Mypagination


class RunTasks(APIView):
    """运行task"""

    # permission_classes = [TokenAuthentication, ]

    def get(self, request, pk, format=None):
        task = PeriodicTask.objects.values("task").get(pk=pk)["task"]
        args = PeriodicTask.objects.values("args").get(pk=pk)["args"]
        kwargs = PeriodicTask.objects.values("kwargs").get(pk=pk)["kwargs"]
        print(task)
        print(args)
        print(kwargs)
        celery_app = current_app
        celery_app.loader.import_default_modules()
        tasks = [(celery_app.tasks.get(task),
                  loads(args),
                  loads(kwargs))]
        print(tasks)
        task_ids = [task.delay(*args, **kwargs)
                    for task, args, kwargs in tasks]
        print(task_ids)
        if 'AsyncResult' in str(task_ids):
            return JsonResponse({'status': 200, 'message': '%s successfully run' % task})

class TasksList(APIView):
    """获取task列表"""
    # permission_classes = [TokenAuthentication, ]

    def get(self, request, format=None):
        celery_app = current_app
        celery_app.loader.import_default_modules()
        tasks = list(sorted(name for name in celery_app.tasks
                            if not name.startswith('celery.')))
        return Response(tasks)
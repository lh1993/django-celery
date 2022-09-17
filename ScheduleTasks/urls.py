# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ScheduleTasks import views


router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'crontab', views.CrontabViewSet)
router.register(r'interval', views.IntervalViewSet)
router.register(r'result', views.ResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tasks-run/<int:pk>/', views.RunTasks.as_view()),
    path('tasks-list', views.TasksList.as_view()),
]
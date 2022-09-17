# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from WeChat import views

router = DefaultRouter()
router.register(r'tag', views.TagInfoViewSet)
router.register(r'agent', views.AgentInfoViewSet)
router.register(r'tagusers', views.TagUsersInfoViewSet)
router.register(r'org', views.OrgInfoViewSet)
router.register(r'employe', views.EmployeInfoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
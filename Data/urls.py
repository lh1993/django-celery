# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Data import views

router = DefaultRouter()
router.register(r'tag', views.TagViewSet)
router.register(r'group', views.TagGroupViewSet)
router.register(r'dbsource', views.DBSourceViewSet)
router.register(r'emailgroup', views.EmailGroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
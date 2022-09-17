"""MyCelery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from DataCenter.oAuth import login, logout, token_check
# from rest_framework.schemas import get_schema_view

# schema_view = get_schema_view(title='DataCenter API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/celery/', include('ScheduleTasks.urls')),
    path('api/wechat/', include('WeChat.urls')),
    path('api/data/', include('Data.urls')),
    path('api/docs/', include_docs_urls(title="数据推送中心")),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token-check/', token_check),
    path('api/login/', login),
    path('api/logout/', logout),
]

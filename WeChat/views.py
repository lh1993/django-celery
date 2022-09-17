from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from DataCenter.oAuth import TokenAuthentication
from WeChat import serializers
from WeChat.models import TagInfo, AgentInfo, TagUsersInfo, EmployeInfo, OrgInfo
# Create your views here.

class TagInfoViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = TagInfo.objects.all()
    serializer_class = serializers.TagInfoSerializer
    # permission_classes = []
    # permission_classes = [TokenAuthentication, ]

class AgentInfoViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = AgentInfo.objects.all()
    serializer_class = serializers.AgentSerializer
    # permission_classes = []

class TagUsersInfoViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = TagUsersInfo.objects.all()
    serializer_class = serializers.TagUsersSerializer
    # permission_classes = []

class OrgInfoViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = OrgInfo.objects.all()
    serializer_class = serializers.OrgSerializer
    # permission_classes = []

class EmployeInfoViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = EmployeInfo.objects.all()
    serializer_class = serializers.EmployeSerializer
    # permission_classes = []
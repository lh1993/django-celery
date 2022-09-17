# -*- coding: utf-8 -*-
from rest_framework import serializers
from WeChat.models import TagInfo, AgentInfo, TagUsersInfo, OrgInfo, EmployeInfo

class  TagInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagInfo
        fields = '__all__'

class  AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentInfo
        fields = '__all__'

class  TagUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagUsersInfo
        fields = '__all__'

class  OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgInfo
        fields = '__all__'

class  EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeInfo
        fields = '__all__'
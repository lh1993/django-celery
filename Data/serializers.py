# -*- coding: utf-8 -*-
from rest_framework import serializers
from Data.models import Tag, TagGroup, DBSource, EmailGroup

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        # fields = ('id', 'name', 'sql', 'group', 'dbsource')
        fields = '__all__'

class TagGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagGroup
        fields = '__all__'

class DBSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBSource
        fields = '__all__'

class EmailGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailGroup
        fields = '__all__'
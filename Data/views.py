from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from DataCenter.oAuth import TokenAuthentication
from Data import serializers
from Data.models import Tag, TagGroup, DBSource, EmailGroup
# Create your views here.

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    # permission_classes = [IsAuthenticated, ]
    # permission_classes = []

class TagGroupViewSet(ModelViewSet):
    queryset = TagGroup.objects.all()
    serializer_class = serializers.TagGroupSerializer
    # permission_classes = []

class DBSourceViewSet(ModelViewSet):
    queryset = DBSource.objects.all()
    serializer_class = serializers.DBSourceSerializer
    # permission_classes = []

class EmailGroupViewSet(ModelViewSet):
    queryset = EmailGroup.objects.all()
    serializer_class = serializers.EmailGroupSerializer
    # permission_classes = []
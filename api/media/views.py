from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import BasicChannelSerializer, ChannelSerializer, ContentSerializer
from .models import Channel, Content


class ChannelViewSet(viewsets.ViewSet):
  queryset = Channel.objects.filter(parent=None)
  serializer_class = BasicChannelSerializer

  def list(self, request, *args, **kwargs):
    if "id" in kwargs:
      self.queryset = Channel.objects.filter(id=kwargs['id'])
      return Response(ChannelSerializer(self.queryset, many=True).data)
    return Response(BasicChannelSerializer(self.queryset, many=True).data)

class ContentViewSet(viewsets.ModelViewSet):
  queryset = Content.objects.all()
  serializer_class = ContentSerializer
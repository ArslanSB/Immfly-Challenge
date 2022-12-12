from rest_framework import serializers

from .models import Channel, Content

class BasicChannelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Channel
    fields = ['id', 'title', 'picture']

class ChannelSerializer(serializers.ModelSerializer):
  content = serializers.SerializerMethodField()
  channels = serializers.SerializerMethodField()

  class Meta:
    model = Channel
    fields = ['id', 'title', 'language', 'picture', 'type', 'content', 'channels']
    depth = 2
  
  def get_content(self, instance):
    showContent = not instance.hasSubChannels()
    if (showContent):
      return ContentSerializer(Content.objects.filter(channel=instance), many=True).data
    return []
  
  def get_channels(self, instance):
    if (instance.hasSubChannels()):
      return BasicChannelSerializer(Channel.objects.filter(parent=instance), many=True).data
    return []


class ContentSerializer(serializers.ModelSerializer):

  class Meta:
    model = Content
    fields = '__all__'
    depth = 2
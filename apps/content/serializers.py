from rest_framework import serializers
from apps.accounts.serializers import ChanelSerializer
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    chanel_name = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['title', 'description', 'author', 'photo', 'file', 'category', 'chanel_name']

    def get_chanel_name(self, obj):
        return ChanelSerializer(instance=obj.author, context={"request": self.context.get("request")}).data

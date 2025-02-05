from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Chanel

class ChanelSerializer(ModelSerializer):
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Chanel
        fields = ['name', 'id', 'user', 'icon', 'desc', 'banner', 'followers_count']

    @staticmethod
    def get_followers_count(obj):
        return obj.followers.all().count()
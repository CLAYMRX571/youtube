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

class ChanelSmallSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_followed = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Chanel
        fields = ['name', 'icon', 'user', 'is_followed', 'followers_count']

    def get_is_followed(self, obj):
        user = self.context.get("request").user
        return user in obj.followers.all()

    @staticmethod
    def get_followers_count(obj):
        return obj.followers.count()
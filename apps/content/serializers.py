from rest_framework import serializers
from apps.accounts.serializers import ChanelSerializer
from .models import Video, Comment, CommentComment, Playlist

class VideoSerializer(serializers.ModelSerializer):
    chanel_name = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['title', 'description', 'author', 'photo', 'file', 'category', 'chanel_name']

    def get_chanel_name(self, obj):
        return ChanelSerializer(instance=obj.author, context={"request": self.context.get("request")}).data

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ["video", "user", "text"]

    def create(self, validated_data):
        user = self.context.get("user")
        validated_data["user"] = user
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.username
        return data

class CommentCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CommentComment
        fields = ["comment", "user", "text"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.username
        return data

class PlaylistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Playlist
        fields = ["user", "videos", "title"]
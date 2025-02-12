from rest_framework import serializers
from apps.accounts.serializers import ChanelSerializer, ChanelSmallSerializer
from .models import Video, Comment, CommentComment, Playlist, CommentLike

class VideoSerializer(serializers.ModelSerializer):
    chanel_name = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['title', 'description', 'author', 'photo', 'file', 'category', 'chanel_name']

    def get_chanel_name(self, obj):
        return ChanelSmallSerializer(instance=obj.author, context={"request": self.context.get("request")}).data

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

class CommentRetrieveSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField() 
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['text', 'user', 'likes_count', 'comments']

    def get_likes_count(self, obj):
        user = self.context.get("request").user
        like = CommentLike.objects.filter(user = user, comment=obj, dislike=False)
        dislike = CommentLike.objects.filter(user = user, comment=obj, dislike=True)
        is_liked = like.exists()
        is_disliked = dislike.exists() 
        data = {
            'is_liked': is_liked,
            'is_disliked': is_disliked,
            'likes': obj.comment_likes.filter(dislike=False).count(),
            'dislikes': obj.comment_likes.filter(dislike=True).count()  
        }
        return data

    def get_comments(self, obj):
        comments = obj.comment_comments
        return CommentCommentSerializer(instance=comments, many=True).data
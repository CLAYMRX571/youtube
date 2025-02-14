from .serializers import VideoSerializer, CommentSerializer, CommentCommentSerializer, PlaylistSerializer, CommentRetrieveSerializer, NewPlaylistSerializer, VideoListSerializer, CategoryListSerializer, CategorySerializer
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, CreateAPIView
from .models import Video, Like, Comment, CommentLike, CommentComment, Playlist, View, Category
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.accounts.serializers import ChanelSmallSerializer
from .permissions import IsHasChanel, IsOwner, IsAuthor
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.models import Chanel
from django.db.models import Count

class CreateVideoView(APIView):
    permission_classes = [IsAuthenticated, IsHasChanel]
    serializer_class = VideoSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        video = serializer.save()
        chanel = request.user.chanel
        video.author = chanel
        video.save()
        data = {
            "status": True,
            "msg": "Video yaratildi",
            "data": self.serializer_class(instance=video, context={"request": request}).data
        }
        return Response(data=data)

class DeleteVideoView(DestroyAPIView):
    permission_classes = [IsOwner]
    serializer_class = VideoSerializer 
    queryset = Video.objects.filter(is_active=True)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        data = {
            "status": True,
            "msg": "Video o'chirildi",
        }
        return Response(data=data)

class UpdateVideoView(UpdateAPIView):
    permission_classes = [IsHasChanel, IsOwner]
    serializer_class = VideoSerializer
    queryset = Video.objects.filter(is_active=True)

class RetrieveVideoView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            video = self.get_object()
            user = request.user
            view = View.objects.get_or_create(video = video, user = user)
            view.save()
        return super().retrieve(request, *args, **kwargs)

class ListVideoView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

class LikeVideoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        like = Like.objects.filter(video=request.data['video'], user=request.user).first()
        video = get_object_or_404(Video, id=request.data['video'])
        dislike = request.data.get('dislike') == "True" 

        if like:
            if like.dislike == dislike:
                like.delete()
                data = {
                    "status": True,
                    "msg": "Like o'chirildi",
                }
            else:
                like.dislike = dislike
                like.save()
                data = {
                    "status": True,
                    "msg": "Like o'zgartirildi",
                }
        else:
            Like.objects.create(video=video, user=request.user, dislike=dislike)
            data = {
                "status": True,
                "msg": "Like qo'shildi",
            }
            return Response(data=data)
        
class CommentVideoView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

class DeleteCommentView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(is_active=True)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        data = {
            "status": True,
            "msg": "Comment o'chirildi",
        }
        return Response(data=data)

class UpdateCommentView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(is_active=True)

class LikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        comment = get_object_or_404(Comment, id=request.data['comment'])
        like = CommentLike.objects.filter(comment=comment, user=request.user).first()
        dislike = request.data.get('dislike') == "True"

        if like:
            if like.dislike == dislike:
                like.delete()
                data = {
                    "status": True,
                    "msg": "Like o'chirildi",
                }
            else:
                like.dislike = dislike
                like.save()
                data = {
                    "status": True,
                    "msg": "Like o'zgartirildi",
                }
        else:
            CommentLike.objects.create(comment=comment, user=request.user, dislike=dislike)
            data = {
                "status": True,
                "msg": "Like qilindi",
            }
            return Response(data=data)

class CommentCommentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCommentSerializer
    queryset = CommentComment.objects.all()

class DeleteCommentCommentView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = CommentCommentSerializer
    queryset = CommentComment.objects.filter(is_active=True)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        data = {
            "status": True,
            "msg": "comment o'chirildi"
        }
        return Response(data=data)

class UpdateCommentCommentView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = CommentCommentSerializer
    queryset = CommentComment.objects.filter(is_active=True)

class CreatePlaylistView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()

class DeletePlaylistView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        data = {
            "status": True,
            "msg": "Playlist o'chirildi"
        }
        return Response(data=data)

class AddVideoPlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        playlist = get_object_or_404(Playlist, id=pk)
        video = get_object_or_404(Video, id=request.data['video'])
        if request.user == playlist.user:
            playlist.videos.add(video)
            data = {
                "status": True,
                "msg": "video qo'shildi"
            }
        else:
            data = {
                "status": False,
                "msg": "Siz playlist egasi emassiz"
            }
        return Response(data=data)

class RemoveVideoPlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        playlist = get_object_or_404(Playlist, id=pk)
        video = get_object_or_404(Video, id=request.data['video'])
        if request.user == playlist.user:
            playlist.videos.remove(video)
            data = {
                "status": True,
                "msg": "video o'chirildi"
            }
        else:
            data = {
                "status": False,
                "msg": "Siz playlist egasi emassiz"
            }
        return Response(data=data)

class FollowChanelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chanel = get_object_or_404(Chanel, id=request.data['chanel'])
        user = request.user
        if user in chanel.followers.all():
            chanel.followers.remove(user)
            data = {
                "status": True,
                "msg": "Chanel removed from follows"
            }
        else:
            chanel.followers.add(user)
            data = {
                "status": True,
                "msg": "Successfully followed"
            }
        return Response(data=data)

class FollowedChanelListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChanelSmallSerializer
    
    def get_queryset(self):
        user = self.request.user
        chanels = user.followed_channels
        return chanels
    
class VideoCommentsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CommentRetrieveSerializer

    def get_queryset(self):
        id = self.kwargs.get('pk')
        video = get_object_or_404(Video, id=id)
        return video.comments 
        
class PlaylistListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NewPlaylistSerializer

    def def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(user=user)
    
class PlaylistRetrieveApiView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        user = self.request.user 
        return Playlist.objects.filter(user=user)

class LikedVideosView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoListSerializer

    def get_queryset(self):
        user = self.request.user 
        likes = Like.objects.filter(user=user, dislike=False)
        return Video.objects.filter(likes__in=likes)
    
class CategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategoryListSerializer
    queryset = Category.objects.filter(is_active=True)

class CategoryRetrieveView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class SearchVideoView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VideoListSerializer

    def get_queryset(self):
        query = self.kwargs.get('query')
        return Video.objects.filter(title__icontains=query).order_by('-created_at')

class OrderByTimeView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VideoListSerializer

    def get_queryset(self):
        return Video.objects.all().order_by('-created_at')

class OrderByviewsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VideoListSerializer  

    def get_queryset(self):
        return Video.objects.annotate(like_count=Count('likes')).order_by('-like_count')

from django.shortcuts import render, get_object_or_404
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsHasChanel, IsOwner, IsAuthor
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VideoSerializer, CommentSerializer, CommentCommentSerializer, PlaylistSerializer
from .models import Video, Like, Comment, CommentLike, CommentComment, Playlist

class CreateVideo(APIView):
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

class DeleteVideo(DestroyAPIView):
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

class UpdateVideo(UpdateAPIView):
    permission_classes = [IsHasChanel, IsOwner]
    serializer_class = VideoSerializer
    queryset = Video.objects.filter(is_active=True)

class RetrieveVideo(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

class ListVideo(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

class LikeVideo(APIView):
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
        
class CommentVideo(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

class DeleteComment(DestroyAPIView):
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

class UpdateComment(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(is_active=True)

class LikeComment(APIView):
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

class DeleteCommentComment(DestroyAPIView):
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

class UpdateCommentComment(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = CommentCommentSerializer
    queryset = CommentComment.objects.filter(is_active=True)

class CreatePlaylist(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer
    queryset = Playlist.objects.all()

class DeletePlaylist(DestroyAPIView):
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

class AddVideoPlaylist(APIView):
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

class RemoveVideoPlaylist(APIView):
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

    

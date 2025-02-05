from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsHasChanel, IsOwner
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VideoSerializer
from .models import Video

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
from django.urls import path
from .views import CreateVideo, DeleteVideo, UpdateVideo, RetrieveVideo, ListVideo

urlpatterns = [
    path('create_video/', CreateVideo.as_view(), name='create_video'),
    path('delete_video/<int:pk>', DeleteVideo.as_view(), name='delete_video'),
    path('update/<int:pk>', UpdateVideo.as_view(), name='update_video'),
    path('retrieve/<int:pk>', RetrieveVideo.as_view(), name='retrieve_video'),
    path('list/', ListVideo.as_view(), name='list_videos'),
]
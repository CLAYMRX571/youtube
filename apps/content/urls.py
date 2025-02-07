from django.urls import path
from .views import CreateVideo, DeleteVideo, UpdateVideo, RetrieveVideo, ListVideo, LikeVideo, CommentVideo, DeleteComment, CommentCommentView, UpdateComment, LikeComment, DeleteCommentComment, UpdateCommentComment, CreatePlaylist, DeletePlaylist, AddVideoPlaylist, RemoveVideoPlaylist

urlpatterns = [
    path('create_video/', CreateVideo.as_view(), name='create_video'),
    path('delete_video/<int:pk>', DeleteVideo.as_view(), name='delete_video'),
    path('update/<int:pk>', UpdateVideo.as_view(), name='update_video'),
    path('retrieve/<int:pk>', RetrieveVideo.as_view(), name='retrieve_video'),
    path('list/', ListVideo.as_view(), name='list_videos'),
    path('like_video/', LikeVideo.as_view(), name='like_video/'),
    path('comment_video/', CommentVideo.as_view(), name='comment_video/'),
    path('update_comment/<int:pk>', UpdateComment.as_view(), name='update_comment/'),
    path('like_comment/', LikeComment.as_view(), name='like_comment/'),
    path('delete_comment_comment/<int:pk>', DeleteCommentComment.as_view(), name='delete_comment_comment/'),
    path('update_comment_comment/<int:pk>', UpdateCommentComment.as_view(), name='update_comment_comment/'),
    path('delete_comment/<int:pk>', DeleteComment.as_view(), name='delete_comment/'),
    path('comment_comment/', CommentCommentView.as_view(), name='comment_comment/'),
    path('create_playlist/', CreatePlaylist.as_view(), name='create_playlist/'),
    path('delete_playlist/<int:pk>', DeletePlaylist.as_view(), name='delete_playlist/'),
    path('add_video_playlist/<int:pk>', AddVideoPlaylist.as_view(), name='add_video_playlist/'),
    path('remove_video_playlist/<int:pk>', RemoveVideoPlaylist.as_view(), name='remove_video_playlist/'),
]
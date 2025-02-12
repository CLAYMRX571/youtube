from django.urls import path
from .views import (CreateVideoView, DeleteVideoView, UpdateVideoView, RetrieveVideoView, 
                    ListVideoView, LikeVideoView, CommentVideoView, DeleteCommentView, CommentCommentView, UpdateCommentView, 
                    LikeCommentView, DeleteCommentCommentView, UpdateCommentCommentView, CreatePlaylistView, DeletePlaylistView, 
                    AddVideoPlaylistView, RemoveVideoPlaylistView, FollowChanelView, FollowedChanelListView, VideoCommentsView)

urlpatterns = [
    path('create_video/', CreateVideoView.as_view(), name='create_video'),
    path('delete_video/<int:pk>', DeleteVideoView.as_view(), name='delete_video'),
    path('update/<int:pk>', UpdateVideoView.as_view(), name='update_video'),
    path('retrieve/<int:pk>', RetrieveVideoView.as_view(), name='retrieve_video'),
    path('list/', ListVideoView.as_view(), name='list_videos'),
    path('like_video/', LikeVideoView.as_view(), name='like_video/'),
    path('comment_video/', CommentVideoView.as_view(), name='comment_video/'),
    path('update_comment/<int:pk>', UpdateCommentView.as_view(), name='update_comment/'),
    path('like_comment/', LikeCommentView.as_view(), name='like_comment/'),
    path('delete_comment_comment/<int:pk>', DeleteCommentCommentView.as_view(), name='delete_comment_comment/'),
    path('update_comment_comment/<int:pk>', UpdateCommentCommentView.as_view(), name='update_comment_comment/'),
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment/'),
    path('comment_comment/', CommentCommentView.as_view(), name='comment_comment/'),
    path('create_playlist/', CreatePlaylistView.as_view(), name='create_playlist/'),
    path('delete_playlist/<int:pk>', DeletePlaylistView.as_view(), name='delete_playlist/'),
    path('add_video_playlist/<int:pk>', AddVideoPlaylistView.as_view(), name='add_video_playlist/'),
    path('remove_video_playlist/<int:pk>', RemoveVideoPlaylistView.as_view(), name='remove_video_playlist/'),
    path('follow_chanel/', FollowChanelView.as_view(), name='follow_chanel'),
    path('followed_chanel/', FollowedChanelListView.as_view(), name='followed_chanel'),
    path('video_comments/<int:pk>', VideoCommentsView.as_view(), name='video_comments'),
]
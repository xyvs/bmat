from django.urls import path

from core import views

urlpatterns = [
    path('add_channel', views.CreateChannelAPIView.as_view(),
         name="add_channel"),
    path('add_performer', views.CreatePerfomerAPIView.as_view(),
         name="add_performer"),
    path('add_song', views.CreateSongAPIView.as_view(),
         name="add_song"),
    path('add_play', views.CreatePlayAPIView.as_view(),
         name="add_play"),
    path('get_song_plays', views.GetSongPlaysAPIView.as_view({'get': 'list'}),
         name="get_song_plays"),
    path('get_channel_plays', views.GetChannelPlaysAPIView.as_view({'get': 'list'}),
         name="get_channel_plays"),
    path('get_top', views.GetTopAPIView.as_view(),
         name="get_top"),
]

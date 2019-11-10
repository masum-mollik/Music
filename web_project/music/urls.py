from django.urls import include, path
from .models import Album, Song
from .import views
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
app_name = 'music'

urlpatterns = [
    # music/
    path('', views.IndexView.as_view(), name='index'),
    # music/177/
    path('<int:pk>/', views.DetailView.as_view(), name='details'),
    # music/album_id/favorite
    path('<int:album_id>/favorite/', views.favorite, name='favorite'),
    # music/create_album
    path('album/create_album/',
         views.AlbumCreateView.as_view(), name='create_album'),
    # music/album/2/update/
    #     This approach applies the decorator on a per-instance basis. If you want every instance of a view to be decorated, you need to take a different approach.
    path('album/<int:pk>/update/',
         login_required(views.AlbumUpdateView.as_view()), name='album-update'),
    # music/album/2/delete/
    path('album/<int:pk>/delete/',
         views.AlbumDeleteView.as_view(), name='album-delete'),
    path('album/<int:pk>/create_song/',
         views.SongCreateView.as_view(), name='create_song'),
    path('album/<int:pk>/<int:song_pk>/',
         views.SongDeleteView.as_view(), name='song-delete'),
    path('list/', views.SongListView.as_view(), name='song_list'),
    path('song/', views.song_detail, name='song_detail'),
]

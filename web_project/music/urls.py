from django.urls import include, path
from .import views
app_name = 'music'

urlpatterns = [
    # music/
    path('', views.index, name='index'),
    # music/177/
    path('<int:album_id>/', views.details, name='details'),
    # music/album_id/favorite
    path('<int:album_id>/favorite/', views.favorite, name='favorite')
]

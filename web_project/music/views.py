from django.http import HttpResponse
from django.shortcuts import render
from .models import Album, Song
from django.shortcuts import get_object_or_404, render


def index(request):
    album_list = Album.objects.all()
    context = {'album_list': album_list}
    return render(request, 'music/index.html', context)


def details(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    context = {'album': album}
    return render(request, 'music/details.html', context)


def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    context = {'album': album,
               'error_message': "you did not selected valid song"}
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/details.html', context)
    else:
        if 'Favorite' in request.POST:
            selected_song.is_favorite = True
            selected_song.save()
            return render(request, 'music/details.html', {'album': album})
        elif 'Unfavorite' in request.POST:
            selected_song.is_favorite = False
            selected_song.save()
            return render(request, 'music/details.html', {'album': album})

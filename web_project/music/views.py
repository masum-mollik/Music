import json
from rest_framework import generics
from django.http import HttpResponse
from django.shortcuts import render
from .models import Album, Song
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .serializers import SongSerializer
decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
class IndexView(generic.ListView):
    model = Album
    template_name = 'music/index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        queryset = Album.objects.filter(user=self.request.user)
        return queryset


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/details.html'

    # To decorate every instance of a class-based view, you need to decorate the class definition itself. To do this you apply the decorator to the dispatch() method of the class
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(DetailView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


@never_cache
@login_required
# decorators = [never_cache, login_required]
# @method_decorator(decorators, name='dispatch') was changed by the above decorators
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


decorators = [never_cache, login_required]


# the line above is similar to the next commented lines
# @method_decorator(never_cache, name='dispatch')
# @method_decorator(login_required, name='dispatch')
@method_decorator(decorators, name='dispatch')
class AlbumCreateView(CreateView):
    model = Album
    template_name = 'music/album_form.html'
    fields = ['artist', 'name', 'genre', 'album_logo']

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(AlbumCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('music:index')


decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
class AlbumUpdateView(UpdateView):
    model = Album
    fields = ['artist', 'name', 'genre', 'album_logo']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('music:index')


decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AlbumDeleteView(DeleteView):
    model = Album
    template_name = 'music/album_confirm_delete.html'
    success_url = reverse_lazy('music:index')

    def delete(self, request, *args, **kwargs):
        # the Post object
        self.object = self.get_object()
        if self.object.User == request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(success_url)
        else:
            return http.HttpResponseForbidden("Invalid delete request")


decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SongCreateView(CreateView):
    model = Song
    template_name = 'music/song_form.html'
    fields = ['file_type', 'song_title', 'file']

    # def form_valid(self, form):
    #     album = self.request.album
    #     form.instance.album = album
    #     return super(SongCreateView, self).form_valid(form)
    def get_initial(self):
        album = get_object_or_404(Album, pk=self.kwargs.get('pk'))
        return {
            'album': album
        }

    def form_valid(self, form):
        album_id = self.kwargs.get('pk')
        form.instance.album_id = album_id
        return super(SongCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('music:index')


decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SongDeleteView(DeleteView):
    model = Song
    template_name = 'music/album_confirm_delete.html'
    success_url = reverse_lazy('music:index')
    pk_url_kwarg = 'song_pk'

    # def delete(self, request, *args, **kwargs):
    #     # the Post object
    #     self.object = self.get_object()
    #     if self.object.User == request.user:
    #         success_url = self.get_success_url()
    #         self.object.delete()
    #         return http.HttpResponseRedirect(success_url)
    #     else:
    #         return http.HttpResponseForbidden("Invalid delete request")


class SongListView(generics.ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = Song.objects.all()
        return queryset


def song_detail(request):
    song = Song.objects.all()
    return render(request, 'music/circleplay.html', {'song': song})

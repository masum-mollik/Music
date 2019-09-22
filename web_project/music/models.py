from django.db import models


class Album(models.Model):
    artist = models.CharField(max_length=250)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    album_logo = models.ImageField(
        upload_to='profile_images/%Y/%m/%d/', max_length=255, blank=True, default='profile_images/default/default.jpg')

    def __str__(self):
        return '"%s %s"' % (self.name, self.artist)


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return'%s %s' % (self.song_title, self.file_type)

from django.db import models
from django.urls import reverse
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from notifications.signals import notify


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    album_logo = models.ImageField(
        upload_to='profile_images/%Y/%m/%d/', max_length=255, blank=True, default='profile_images/default/default.jpg')
    created_at = models.DateTimeField(default=timezone.now())
    last_updated = models.DateTimeField(null=True)

    def __str__(self):
        return '"%s - %s"' % (self.name, self.artist)

    def save(self):
        if not self.id:
            self.created_at = timezone.now()
        self.last_updated = timezone.now()
        super(Album, self).save()

    def was_published_recently(self):
        if self.created_at >= timezone.now() - datetime.timedelta(seconds=20):
            return 'Just now'
        elif self.created_at >= timezone.now() - datetime.timedelta(minutes=1):
            return str((timezone.now() - self.created_at).seconds) + ' seconds ago'
        elif self.created_at >= timezone.now() - datetime.timedelta(minutes=60):
            return str(int((timezone.now() - self.created_at).seconds/60)) + ' minutes ago'
        elif self.created_at >= timezone.now() - datetime.timedelta(hours=24):
            return str(int((timezone.now() - self.created_at).seconds/3600)) + ' hours ago'
        elif self.created_at >= timezone.now() - datetime.timedelta(days=365):
            return str((timezone.now() - self.created_at).days) + ' days ago'
        else:
            return 'Created at: ' + str(self.created_at.year)+'-'+str(self.created_at.month)+'-'+str(self.created_at.day)+' ' + str(self.created_at.hour) + ':'+str(self.created_at.minute) + ':' + str(self.created_at.second)


def album_handler(sender, instance, created, **kwargs):
    notify.send(instance.user, recipient=instance.user, verb='was saved')


post_save.connect(album_handler,  sender=Album)


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    free = models.BooleanField(default=True)
    mp3 = models.FileField(upload_to='music/%Y/%m/%d')
    oga = models.FileField(upload_to='music/%Y/%m/%d', null=True)
    file_type = models.CharField(max_length=10)
    # song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return'%s - %s' % (self.title, self.file_type)


def song_handler(sender, instance, created, **kwargs):
    notify.send(instance.album.user,
                recipient=instance.album.user, verb='was saved')


post_save.connect(song_handler,  sender=Song)

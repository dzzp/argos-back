from django.db import models
from django.contrib.postgres.fields import ArrayField

from video.validators import lnglat_validator


class Video(models.Model):
    _id = models.AutoField(primary_key=True)
    video_path = models.TextField(unique=True)
    running_time = models.IntegerField()    # Second
    frame = models.CharField(max_length=16, default='0')

    def __str__(self):
        return str(self._id)


class SubVideo(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    location = models.CharField(
        max_length=50,
        blank=True,
        validators=[lnglat_validator],
        help_text='Please input "lng,lat" format'
    )
    time = models.DateTimeField()


class DataSet(models.Model):
    _id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    coordinate = ArrayField(models.CharField(max_length=8))
    time = models.DateTimeField()

    def __str__(self):
        return str(self._id)

from django.db import models
from django.contrib.postgres.fields import ArrayField

from video.validators import lnglat_validator


class Video(models.Model):
    _id = models.AutoField(primary_key=True)
    video_path = models.TextField(unique=True)
    time = models.DateTimeField(auto_now=True)
    location = models.CharField(
        max_length=50,
        blank=True,
        validators=[lnglat_validator],
        help_text='Please input "lng,latt" format'
    )


    def __str__(self):
        return str(self._id)


class TestVideo(models.Model):
    video = models.FileField(upload_to='assets/')

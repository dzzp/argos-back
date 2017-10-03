from django.db import models
from django.contrib.postgres.fields import ArrayField


class Video(models.Model):
    _id = models.AutoField(primary_key=True)
    video_path = models.TextField(unique=True)
    time = models.DateTimeField()
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)

    def __str__(self):
        return str(self._id)


class Person(models.Model):
    _id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    bbox_path = models.TextField()
    feature_path = models.TextField()
    time = models.DateTimeField()

class TestVideo(models.Model):
    video = models.FileField(upload_to='assets/')

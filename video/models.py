import time
import hashlib

from django.db import models


def _generateHash():
     now = str(time.time()).encode('utf-8')
     hash_value = hashlib.sha1(now)
     return hash_value.hexdigest()[:7]


class Video(models.Model):
    _id = models.AutoField(primary_key=True)
    hash_value = models.CharField(max_length=7, default=_generateHash, unique=True)
    video_path = models.TextField()
    time = models.DateTimeField()
    memo = models.TextField(blank=True)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    total_frame = models.IntegerField(default=0)
    frame_rate = models.IntegerField(default=0)

    def __str__(self):
        return str(self.hash_value)


class Person(models.Model):
    _id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    person_path = models.FilePathField()
    feature_path = models.FilePathField()
    score = models.FloatField()
    frame_num = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self._id)


class TestVideo(models.Model):
    video = models.FileField(upload_to='assets/')

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Video(models.Model):
    _id = models.AutoField(primary_key=True)
    video_path = models.TextField()
    running_time = models.DateTimeField()

    def __str__(self):
        return str(self._id)


class DataSet(models.Model):
    _id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    coordinate = ArrayField(models.CharField(max_length=8))
    time = models.DateTimeField()

    def __str__(self):
        return str(self._id)

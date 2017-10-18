from django.db import models


class Video(models.Model):
    _id = models.AutoField(primary_key=True)
    video_path = models.FilePathField(allow_files=True, path="/")
    time = models.DateTimeField()
    memo = models.TextField(blank=True)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    total_frame = models.IntegerField(default=0)
    frame_rate = models.IntegerField(default=0)

    def __str__(self):
        return str(self._id)


class Person(models.Model):
    _id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    person_path = models.FilePathField()
    feature_path = models.FilePathField()
    score = models.FloatField()
    frame_num = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class TestVideo(models.Model):
    video = models.FileField(upload_to='assets/')

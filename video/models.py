from django.db import models
from video.validators import validate_file_extension


class Video(models.Model):
    _id = models.AutoField(primary_key=True)
    video = models.FileField(
        upload_to='static/',
        validators=[validate_file_extension]
    )
    running_time = models.DateTimeField()


class DataSet(models.Model):
    _id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    coordinate = models.ArrayField(models.CharField(max_length=8))
    time = models.DateTimeField()

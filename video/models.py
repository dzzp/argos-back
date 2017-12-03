import time
import hashlib

from django.db import models
from django.contrib.postgres.fields import ArrayField


def _generateHash():
    now = str(time.time()).encode('utf-8')
    hash_value = hashlib.sha1(now)
    return hash_value.hexdigest()[:7]


class Case(models.Model):
    _id = models.AutoField(primary_key=True)
    case_title = models.CharField(max_length=50)
    case_path = models.FilePathField(blank=True)
    group_hash_id = models.CharField(
        max_length=8,
        default=_generateHash,
        unique=True
    )
    generated_datetime = models.DateTimeField(auto_now_add=False)
    memo = models.TextField(blank=True)

    def __str__(self):
        return str(self._id)


class Video(models.Model):
    _id = models.AutoField(primary_key=True)
    case = models.ForeignKey('Case', on_delete=models.CASCADE)
    hash_value = models.CharField(
        max_length=7, default=_generateHash, unique=True
    )
    video_path = models.FilePathField()
    date = models.DateField(default='0001-01-01')
    time = models.TimeField(default='00:00:00')
    memo = models.TextField(blank=True)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    total_frame = models.IntegerField(default=0)
    frame_rate = models.IntegerField(default=0)
    is_detect_done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.hash_value)


class Person(models.Model):
    _CHOICES = (
        ('U', 'Undefined'),
        ('P', 'Positive'),
        ('N', 'Negative'),
    )

    _id = models.AutoField(primary_key=True)
    hash_value = models.CharField(
        max_length=7, default=_generateHash, unique=True
    )
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    person_path = models.FilePathField()
    score = models.FloatField()
    frame_num = models.IntegerField()
    shot_time = models.TimeField(auto_now_add=False)
    status = models.CharField(
        max_length=1,
        choices=_CHOICES,
        default='U',
    )

    def __str__(self):
        return str(self._id)


class ProbeList(models.Model):
    _id = models.AutoField(primary_key=True)
    case = models.ForeignKey('Case', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    def __str__(self):
        return str(self._id)


class TestVideo(models.Model):
    video = models.FileField(upload_to='assets/')


class LoadList(models.Model):
    case = models.ForeignKey('Case', models.CASCADE)
    total = ArrayField(models.CharField(max_length=7), default=list)
    current = models.CharField(max_length=7)

    def __str__(self):
        return str(self.case.group_hash_id)

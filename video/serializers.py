from rest_framework import serializers
from video.models import Video, Person


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('video_path', 'time', 'lat', 'lng',)


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('video', 'bbox_path', 'feature_path', 'time',)

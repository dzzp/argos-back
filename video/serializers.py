import os

from rest_framework import serializers
from django.core.exceptions import ValidationError
from video.models import Video, Person


class VideoSerializer(serializers.ModelSerializer):
    def is_exists(self, file_path):
        if os.path.isfile(file_path):
            return True
        else:
            return False


    def validate(self, data):
        file_types = ('mov', '.mp4', '.avi')
        file_ext = os.path.splitext(data['video_path'])

        if file_ext[-1] in file_types:
            if self.is_exists(data['video_path']):
                return data
            else:
                raise serializers.ValidationError({
                    'message': 'File does not exist',
                    'path': data['video_path']
                }, code='error')
        else:
            raise serializers.ValidationError({
                'message:': 'Filetype error occured',
                'type': file_ext
            }, code='error')


    class Meta:
        model = Video
        fields = ('video_path', 'time', 'memo', 'lat', 'lng',)
        #validators = []


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('video', 'bbox_path', 'feature_path', 'time',)

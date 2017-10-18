import os

from rest_framework import status, serializers
from rest_framework.exceptions import ErrorDetail

from video.models import Video, Person


class VideoSerializer(serializers.ModelSerializer):
    def _is_exists(self, file_path):
        if os.path.isfile(file_path):
            return True
        else:
            return False

    @property
    def errors(self):
        ret = super(serializers.Serializer, self).errors
        if isinstance(ret, list) and len(ret) ==1 and getattr(ret[0], 'code', None) =='null':
            detail = ErrorDetail('No data provided', code='null')
            ret = {api_settings.NON_FIELD_ERRORS_KEY: detail}
        for key, value in ret.items():
            ret[key] = value[0]
        return ret

    def validate(self, data):
        file_types = ('mov', '.mp4', '.avi')
        file_ext = os.path.splitext(data['video_path'])

        if file_ext[-1] in file_types:
            if not self._is_exists(data['video_path']):
                raise serializers.ValidationError({
                    'message': 'File does not exist',
                    'video_path': data['video_path'],
                }, code='error')
        else:
            raise serializers.ValidationError({
                'message': 'Filetype error occured',
                'file_type': file_ext[-1],
            }, code='error')

    class Meta:
        model = Video
        #fields = ('video_path', 'time', 'memo', 'lat', 'lng',)
        fields = '__all__'
        extra_kwargs = {'video_path': {'allow_files': True}}


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('video', 'bbox_path', 'feature_path', 'time',)

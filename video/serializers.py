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
        if isinstance(ret, list) and len(ret) == 1 and getattr(ret[0], 'code', None) =='null':
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
        return data

    class Meta:
        model = Video
        fields = ('video_path', 'time', 'memo', 'lat', 'lng',)


'''
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('video', 'person_path', 'feature_path', 'score', 'frame_num', 'time',)
'''

class PersonSerializer:
    _person_list = []

    def __init__(self, person_data):
        for person in person_data:
            self._person_list.append(Person.objects.create(
                video=person['video'],
                person_path=person['person_path'],
                feature_path=person['feature_path'],
                score=person['score'],
                frame_num=person['frame_num'],
                time=person['time'],
            ))

    def getPersonList(self):
        result = dict()
        result['code'] ='detect_response'
        result['videos'] = list()

        for person in self._person_list:
            video = person.video
            data = {
                'lat': video.lat,
                'lng': video.lng,
                'path': video.video_path,
                'memo': video.memo,
            }

            data['imgs'] = list()
            

            result['videos'].append()

        return result

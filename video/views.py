import json

from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from video.models import VideoGroup, Video, LoadList
from video.frame_worker import extract_video_frame_array
from video.serializers import VideoSerializer, PersonSerializer
from data_picker.tools import response_code, response_detect


@api_view(['POST'])
def detection(request):
    video_list = []
    video_hash_list = []
    for video in request.data['videos']:
        serializer = VideoSerializer(data=video)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        video_obj = serializer.save()
        video_list.append(video_obj)
        video_hash_list.append(video_obj.hash_value)
    serialized_videos = extract_video_frame_array(video_list)
    #VideoGroup.objects.create(video_hash_list=video_hash_list)
    
    return Response(response_detect(serialized_videos))


@api_view(['POST'])
def probe(request):
    person_list = request.data['persons']
    executing_probe(person_list)
    return Response(json.dumps({"code": "ok"}))


@api_view(['GET', 'POST'])
def processing(request):
    if request.data['code'] == 'is_detect':
        #group = request.data['video_group_hash']
        load = LoadList.objects.all()[0]
        data = {
            'current': load.current,
            'total': load.total,
            'video': load.video,
            'code': 'processing_detect'
        }
        return Response(json.dumps(data))
    else:
        return Response(response_code('processing_reid'))

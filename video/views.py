from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from video.models import Video
from video.frame_worker import extract_video_frame_array
from video.serializers import VideoSerializer, PersonSerializer
from data_picker.tools import response_code, response_detect


@api_view(['POST'])
def detection(request):
    video_list = []
    for video in request.data['videos']:
        serializer = VideoSerializer(data=video)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        video_list.append(serializer.save())
    serialized_videos = extract_video_frame_array(video_list)
    
    return Response(response_detect(serialized_videos))


@api_view(['GET'])
def processing(request):
    if request.data['code'] == 'is_detect':
        return Response(response_code('processing_detect'))
    else:
        return Response(response_code('processing_reid'))

from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from video.models import Video
from video.serializers import VideoSerializer, PersonSerializer
from data_picker.tools import response_code


@api_view(['POST'])
def detection(request):
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(response_code('processing_detect'))
    return Response(serializer.errors, status=status.HTTP400_BAD_REQUEST)


@api_view(['GET'])
def processing(request):
    print(request)
    return Response(request_code('processing_reid'))
    #return Response(response_code('processing_detect'))

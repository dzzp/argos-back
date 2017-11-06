import os
import json
import multiprocessing
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from video.models import Case, Video, LoadList
from video.frame_worker import extract_video_frame_array
from video.probe_worker import feature_extract 
from video.serializers import VideoSerializer, PersonSerializer
from data_picker.tools import response_code, response_detect


@api_view(['GET', 'POST'])
def cases(request):
    # GET
    if request.method == 'GET':
        search_query = request.query_params.get('search')
        if search_query is None:
            return Reponse()

        cases = Case.objects.filter(case_title=search_query)
        result = dict()
        result['cases'] = []
        for case in cases:
            result['cases'].append({
                'title': case.case_title,
                'hash': case.group_hash_id,
                'memo': case.memo,
                'datetime': case.generated_datetime,
            })
        return Response(json.dumps(result))

    # POST
    else:
        case = Case.objects.create(
            title=request.data['title'],
            memo=request.data['memo'],
            generated_datetime=request.data['datetime'],
        )
        return Response(json.dumps({
            'title': request.data['title'],
            'memo': request.data['memo'],
            'datetime': request.data['datetime'],
            'hash': case.group_hash_id,
        }))

@api_view(['GET', 'POST'])
def cases_hash_videos(request, case_hash):
    # GET
    if request.method == 'GET':
        try:
            case = Case.objects.get(group_hash_id=case_hash)
            result = dict()
            result['videos'] = []
            for video_hash in case.video_hash_list:
                video = Video.objects.get(hash_value=video_hash)
                data = {
                    'path': video.video_path,
                    'hash': video.hash_value,
                    'imgs': []
                }

                person_list = Person.objects.filter(video=video).order_by('shot_datetime')
                shot_datetime_list = set()
                for person in person_list:
                    shot_datetime_list.add(person.shot_datetime)
                for shot_datetime in shot_datetime_list:
                    person_list = Person.objects.filter(shot_datetime=shot_datetime)

                    person_data = dict()
                    person_data['datetime'] = shot_datetime
                    person_data['persons'] = []

                    for person in person_list:
                        person_data['persons'].append({
                            'hash': person.hash_value,
                            'bbox_path': person.person_path,
                            'orig_path': 'temp',
                        })
                    data['imgs'].append(person_data)
                result['videos'].append(data)
            return Response(json.dumps(result))

        except:
            return Response()

    # POST
    else:
        for video in request.data['videos']:
            Video.objects.create(
                video_path=video['path'],
                memo=video['memo']
            )
        return Response(json.dumps({'code': 'ok'}))


@api_view(['GET', 'POST'])
def cases_hash_probes(request, case_hash):
    # GET
    if request.method == 'GET':
        case = Case.objects.get(group_hash_id=case_hash)
        video_hash_list = case.video_hash_list

        result = dict()
        result['persons'] = []
        for video_hash in video_hash_list:
            video = Video.objects.get(hash_value=video_hash)
            person_list = Person.objects.filter(video=video)

            for person in person_list:
                result['persons'].append({
                    'person_hash': person.hash_value,
                    'video_hash': video.hash_value,
                    'bbox_path': person.person_path,
                    'orig_path': 'temp',
                })

        return Response(json.dumps(result))

    # POST
    else:
        person_hash_list = request.data['persons']
        for person_hash in person_hash_list:
            person = Person.objects.get(hash_value=person_hash)
        return Response(json.dumps({'code': 'ok'}))


@api_view(['GET'])
def cases_hash_galleries(request, case_hash):
    case = Case.objects.get(group_hash_id=case_hash)
    video_hash_list = case.video_hash_list

    result = dict()
    result['persons'] = []
    for video_hash in video_hash_list:
        video = Video.objects.get(hash_value=video_hash)
        person_list = Person.objects.filter(video=video)

        for person in person_list:
            result['persons'].append({
                'person_hash': person.hash_value,
                'video_hash': video.hash_value,
                'bbox_path': person.person_path,
                'orig_pash': 'temp',
            })

        return Response(json.dumps(result))


@api_view(['POST'])
def detection(request):
    video_list = []
    video_hash_list = []
    for video in request.data['videos']:
        serializer = VideoSerializer(data=video)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        video_obj = serializer.save()
        video_list.append(video_obj)
        video_hash_list.append(video_obj.hash_value)

    '''
    result = multiprocessing.Queue()
    proc = multiprocessing.Process(target=extract_video_frame_array, args=(video_list, result))
    proc.start()
    proc.join()
    serialized_videos = result.get()
    '''

    serialized_videos = extract_video_frame_array(video_list)
    video_group = VideoGroup.objects.create(video_hash_list=video_hash_list)
    
    return Response(
        response_detect(serialized_videos, video_group.group_hash_id)
    )


@api_view(['POST'])
def probe(request):
    group_id = request.data['group_id']
    video_group = VideoGroup.objects.get(group_hash_id=group_id)
    video_list = video_group.video_hash_list
    for video in video_list:
        temp = Video.objects.get(hash_value=video)
        temp_path = temp.video_path 
        feature_extract(os.path.join(temp_path, 'bbox'))
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

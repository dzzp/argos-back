import os
import json
import numpy as np

from annoy import AnnoyIndex

from rest_framework.response import Response
from rest_framework.decorators import api_view

from video.models import Case, Video, Person
from video.frame_worker import extract_video_frame_array
# from video.serializers import VideoSerializer, PersonSerializer
# from data_picker.tools import response_code, response_detect


@api_view(['GET', 'POST'])
def cases(request):
    # GET
    if request.method == 'GET':
        search_query = request.query_params.get('search')
        if search_query == '':
            cases = Case.objects.all().order_by('generated_datetime')[:5]
            result = dict()
            result['cases'] = []
            for case in cases:
                result['cases'].append({
                    'title': case.case_title,
                    'hash': case.group_hash_id,
                    'memo': case.memo,
                    'datetime': str(case.generated_datetime),
                })
            return Response(json.dumps(result))

        cases = Case.objects.filter(case_title=search_query)
        result = dict()
        result['cases'] = []
        for case in cases:
            result['cases'].append({
                'title': case.case_title,
                'hash': case.group_hash_id,
                'memo': case.memo,
                'datetime': str(case.generated_datetime),
            })
        return Response(json.dumps(result))

    # POST
    else:
        case = Case.objects.create(
            case_title=request.data['title'],
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
        except:
            return Response(json.dumps({'error': 'error'}))
        result = dict()
        result['videos'] = []
        for video_hash in case.video_hash_list:
            video = Video.objects.get(hash_value=video_hash)
            data = {
                'path': video.video_path,
                'hash': video.hash_value,
                'imgs': []
            }

            shot_time_list = Person.objects.filter(
                video=video
            ).distinct('shot_time')
            for shot_time in shot_time_list:
                person_list = Person.objects.filter(
                    video=video, shot_time=shot_time.shot_time
                )
                person_data = dict()
                person_data['datetime'] = str(shot_time.shot_time)
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

    # POST
    else:
        case = Case.objects.get(group_hash_id=case_hash)

        video_list = []
        video_hash_list = []
        for video in request.data['videos']:
            video_obj = Video.objects.create(
                video_path=video['path'],
                memo=video['memo']
            )
            video_list.append(video_obj)
            video_hash_list.append(video_obj.hash_value)
        case.video_hash_list = video_hash_list
        case.save()
        extract_video_frame_array(video_list)
        return Response(json.dumps({'code': 'ok'}))


@api_view(['GET', 'PUT'])
def cases_hash_videos_hash(request, case_hash, video_hash):
    # GET
    if request.method == 'GET':
        video = Video.objects.get(hash_value=video_hash)
        result = {
            'memo': video.memo,
            'lat': video.lat,
            'lng': video.lng,
            'datetime': str(video.time),    # TEMP
            }

        return Response(json.dumps(result))

    # PUT
    else:
        video = Video.objects.get(hash_value=video_hash)
        video.memo = request.data['memo']
        video.lat = request.data['lat']
        video.lng = request.data['lng']
        video.time = request.data['datetime']    # TEMP
        video.save()

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
        # THIS IS GALLERY HOHO
        case = Case.objects.get(group_hash_id=case_hash)
        video_hash_list = case.video_hash_list

        feat_list = np.array([])
        total_file_list = []
        total_node = 0
        for video_hash in video_hash_list:
            video = Video.objects.get(hash_value=video_hash)
            base_path = os.path.split(video.video_path)
            file_name = os.path.splitext(base_path[-1])[0]
            feat_path = os.path.join(
                base_path[0], video.hash_value + '_' + file_name
            )
            feat = np.load(os.path.join(feat_path, 'feat', 'features.npy'))
            file_list = os.path.join(feat_path, 'feat', 'file_list.txt')
            with open(file_list, 'r') as f:
                file_list = f.readlines()
                file_list = [l.strip().split()[0] for l in file_list]
                total_node += len(file_list)
            if feat_list.shape == np.array([]).shape:
                feat_list = feat
            else:
                feat_list = np.concatenate((feat_list, feat), axis=0)

            for file_name in file_list:
                total_file_list.append(file_name)

        tree = AnnoyIndex(feat_list.shape[1], metric='euclidean')
        for i in range(len(total_file_list)):
            tree.add_item(i, feat_list[i])
        tree.build(100)

        person_hash_list = request.data['persons']
        candidates_dict = dict()
        for person_hash in person_hash_list:
            person = Person.objects.get(hash_value=person_hash)
            person_index = total_file_list.index(person.person_path)
            person_feat = feat_list[person_index]

            candidates, scores = tree.get_nns_by_vector(
                person_feat, 1000, include_distances=True
            )
            for index, cand in enumerate(candidates):
                if not cand in candidates_dict:
                    candidates_dict[cand] = list()
                candidates_dict[cand].append(scores[index])
        candidates_list = [(total_file_list[i], sum(candidates_dict[i])/len(candidates_dict[i])) for i in candidates_dict.keys()]
        candidates_list.sort(key=lambda x: x[1])
        candidates_list = candidates_list[:100]
        print(candidates_list)

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
                'orig_path': 'temp',
            })

        return Response(json.dumps(result))


'''
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

    serialized_videos = extract_video_frame_array(video_list)
    video_group = Case.objects.create(video_hash_list=video_hash_list)

    return Response(
        response_detect(serialized_videos, video_group.group_hash_id)
    )


@api_view(['POST'])
def probe(request):
    group_id = request.data['group_id']
    video_group = Case.objects.get(group_hash_id=group_id)
    video_list = video_group.video_hash_list
    for video in video_list:
        temp = Video.objects.get(hash_value=video)
        temp_path = temp.video_path
        feature_extract(os.path.join(temp_path, 'bbox'))
    return Response(json.dumps({"code": "ok"}))


@api_view(['GET', 'POST'])
def processing(request):
    if request.data['code'] == 'is_detect':
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
'''

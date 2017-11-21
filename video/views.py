import os
import numpy as np

from annoy import AnnoyIndex
from datetime import datetime
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view

from data_picker.tools import get_origin_path
from video.frame_worker import extract_video_frame_array
from video.models import Case, Video, Person, ProbeList, LoadList


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
            return Response(data=result)

        cases = Case.objects.filter(
            case_title=search_query
        ).order_by('generated_datetime')
        result = dict()
        result['cases'] = []
        for case in cases:
            result['cases'].append({
                'title': case.case_title,
                'hash': case.group_hash_id,
                'memo': case.memo,
                'datetime': str(case.generated_datetime),
            })
        return Response(data=result)

    # POST
    else:
        base_path = os.path.join(settings.BASE_DIR, 'assets')

        try:
            case = Case.objects.create(
                case_title=request.data['title'],
                memo=request.data['memo'],
                generated_datetime=request.data['datetime'],
            )
        except Exception as e:
            return Response(data={'error': 'error'})
        case_path = os.path.join(base_path, case.group_hash_id)
        os.mkdir(case_path)
        case.case_path = case_path
        case.save()

        LoadList.objects.create(case=case.group_hash_id)

        return Response(data={
            'title': request.data['title'],
            'memo': request.data['memo'],
            'datetime': request.data['datetime'],
            'hash': case.group_hash_id,
        })


@api_view(['GET', 'POST'])
def cases_hash_videos(request, case_hash):
    # GET
    if request.method == 'GET':
        try:
            case = Case.objects.get(group_hash_id=case_hash)
        except:
            return Response(data={'error': 'error'})

        result = dict()
        result['videos'] = []
        video_list = Video.objects.filter(case=case)
        for video in video_list:
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
                    orig_path = get_origin_path(
                        case.case_path, person.person_path
                    )

                    person_data['persons'].append({
                        'hash': person.hash_value,
                        'bbox_path': person.person_path,
                        'orig_path': orig_path,
                    })
                data['imgs'].append(person_data)
            result['videos'].append(data)
        return Response(data=result)

    # POST
    else:
        case = Case.objects.get(group_hash_id=case_hash)

        video_list = []
        for video in request.data['videos']:
            video_obj = Video.objects.create(
                case=case,
                video_path=video['path'],
                memo=video['memo']
            )
            video_list.append(video_obj)
        extract_video_frame_array(case_hash, video_list)
        return Response(data={'code': 'ok'})


@api_view(['GET', 'PUT'])
def cases_hash_videos_hash(request, case_hash, video_hash):
    # GET
    if request.method == 'GET':
        video = Video.objects.get(hash_value=video_hash)
        shot_datetime = video.date + video.time
        result = {
            'memo': video.memo,
            'lat': video.lat,
            'lng': video.lng,
            'datetime': str(shot_datetime),    # TEMP
        }

        return Response(data=result)

    # PUT
    else:
        datetime_data = datetime.strptime(request.data['datetime'], '%Y-%m-%dT%H:%M:%S')

        video = Video.objects.get(hash_value=video_hash)
        video.memo = request.data['memo']
        video.lat = request.data['lat']
        video.lng = request.data['lng']
        video.date = datetime_data.date()
        video.time = datetime_data.time()
        video.save()

        return Response(data={'code': 'ok'})


@api_view(['GET', 'POST'])
def cases_hash_probes(request, case_hash):
    # GET
    if request.method == 'GET':
        case = Case.objects.get(group_hash_id=case_hash)

        result = dict()
        result['persons'] = []
        probe_list = ProbeList.objects.filter(case=case)

        for probe in probe_list:
            orig_path = get_origin_path(
                case.case_path, probe.person.person_path
            )

            result['persons'].append({
                'person_hash': probe.person.hash_value,
                'video_hash': probe.person.video.hash_value,
                'bbox_path': probe.person.person_path,
                'orig_path': orig_path,
            })

        return Response(data=result)

    # POST
    else:
        case = Case.objects.get(group_hash_id=case_hash)
        person_hash_list = request.data['persons']

        # Reset probe list
        probe_check = ProbeList.objects.all()
        if probe_check.count() > 0:
            probe_check.delete()

        for person_hash in person_hash_list:
            person = Person.objects.get(hash_value=person_hash)
            ProbeList.objects.create(case=case, person=person)
        return Response(data={'code': 'ok'})


@api_view(['GET'])
def cases_hash_galleries(request, case_hash):
    case = Case.objects.get(group_hash_id=case_hash)
    video_list = Video.objects.filter(case=case)
    person_list = []

    feat_path = os.path.join(case.case_path, 'feat_list.npy')
    total_list_path = os.path.join(case.case_path, 'total_list.txt')
    tree_path = os.path.join(case.case_path, 'galleries.ann')

    try:
        feat_list = np.load(feat_path)
        with open(total_list_path, 'r') as f:
            total_file_list = [line.strip() for line in f.readlines()]
    except:
        feat_list = np.array([])
        total_file_list = []
        total_node = 0
        for video in video_list:
            folder_name = '%s_%s' % (
                video.hash_value,
                os.path.splitext(os.path.basename(video.video_path))[0]
            )
            base_path = os.path.join(case.case_path, folder_name)

            feat = np.load(os.path.join(base_path, 'feat', 'features.npy'))
            file_list = os.path.join(base_path, 'feat', 'file_list.txt')
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
            persons = Person.objects.filter(video=video)
            for person in persons:
                person_list.append(person)

        np.save(feat_path, feat_list)
        with open(total_list_path, 'w') as f:
            f.writelines('%s\n' % file_item for file_item in total_file_list)

        tree = AnnoyIndex(feat_list.shape[1], metric='euclidean')
        for i in range(len(total_file_list)):
            tree.add_item(i, feat_list[i])
        tree.build(100)
        tree.save(tree_path)

    tree = AnnoyIndex(feat_list.shape[1], metric='euclidean')
    tree.load(tree_path)

    candidates_dict = dict()
    result = dict()
    result['persons'] = []

    probe_list = ProbeList.objects.filter(case=case)
    for probe in probe_list:
        person_index = total_file_list.index(probe.person.person_path)
        person_feat = feat_list[person_index]

        candidates, distances = tree.get_nns_by_vector(
            person_feat, 1000, include_distances=True
        )
        for index, cand in enumerate(candidates):
            # same image
            if person_index == cand:
                continue
            if not cand in candidates_dict:
                candidates_dict[cand] = list()
            candidates_dict[cand].append(distances[index])
    candidates_list = [(total_file_list[i], min(candidates_dict[i])) for i in candidates_dict.keys()]
    candidates_list.sort(key=lambda x: x[1])
    candidates_list = candidates_list[:100]

    for candidate, distance in candidates_list:
        person = Person.objects.get(person_path=candidate)
        orig_path = get_origin_path(
            case.case_path, person.person_path
        )

        result['persons'].append({
            'person_hash': person.hash_value,
            'video_hash': person.video.hash_value,
            'bbox_path': person.person_path,
            'orig_path': orig_path,
            'distance': distance
        })

    return Response(data=result)


@api_view(['GET', 'POST'])
def processing(request, case_hash):
    load = LoadList.objects.get(case=case_hash)
    data = {
        'current': load.current,
        'total': load.total,
        'video': load.video,
        'code': 'processing_detect'
    }
    return Response(data=data)

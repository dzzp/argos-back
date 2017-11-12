import os
import av
import datetime
import skvideo.io
import numpy as np
import multiprocessing

from PIL import Image, ImageDraw

from video.models import Video, Person, LoadList
from video.calculation import NumericStringParser
from object_detection.main import detect_person

from video.probe_worker import feature_extract


_NUM_STR_PARSER = NumericStringParser()


def calculate_string_exp(data):
    return round(_NUM_STR_PARSER.eval(data))


def extract_video_metadata(hash_value):
    video_obj = Video.objects.get(hash_value=hash_value)
    video = skvideo.io.ffprobe(video_obj.video_path)

    metadata = {
        'total_frame': int(video['video']['@nb_frames']),
        'frame_rate': calculate_string_exp(video['video']['@avg_frame_rate']),
        'hash_value': video_obj.hash_value,
    }

    video_obj.total_frame = int(video['video']['@nb_frames'])
    video_obj.frame_rate = calculate_string_exp(
        video['video']['@avg_frame_rate']
    )
    video_obj.save()

    return metadata


def save_video_frame(hash_value, frames, bbox_list):
    video = Video.objects.get(hash_value=hash_value)
    file_path = os.path.join(
        video.case.case_path,
        '%s_%s' % (
            video.hash_value,
            os.path.splitext(os.path.basename(video.video_path))[0]
        )
    )

    idx = 0
    for frame_idx in range(len(frames)):
        origin_img = Image.fromarray(frames[frame_idx])
        draw = ImageDraw.Draw(origin_img)
        img_idx = 0

        for bbox, score in bbox_list[frame_idx]:
            person_name = os.path.join(
                file_path, 'bbox', '%d_%d.jpg' % (idx, img_idx)
            )

            crop_img = origin_img.crop(bbox)
            crop_img.save(person_name)
            draw.rectangle(bbox, outline='red')

            img_idx += 1
            shot_time = (
                datetime.datetime.combine(
                    datetime.date(1, 1, 1), video.time
                ) + datetime.timedelta(seconds=frame_idx)
            ).time()

            Person.objects.create(
                video=video,
                person_path=person_name,
                score=score,
                frame_num=video.frame_rate*frame_idx,
                shot_time=shot_time,
            )

            origin_img.save(os.path.join(file_path, 'origin', '%d.jpg' % idx))
        idx += 1


def extract_video_frame_array(videos):
    load = LoadList.objects.all()[0]
    load.total = len(videos)
    load.current = 0
    load.save()

    for video in videos:
        load.video = video.video_path
        load.current = load.current + 1
        load.save()

        case_path = video.case.case_path
        folder_name = '%s_%s' % (
            video.hash_value,
            os.path.splitext(os.path.basename(video.video_path))
        )
        case_video_path = os.path.join(case_path, folder_name)
        try:
            os.mkdir(os.path.join(case_video_path, 'origin'))
            os.mkdir(os.path.join(case_video_path, 'bbox'))
            os.mkdir(os.path.join(case_video_path, 'feat'))
        except Exception as e:
            print('Folder already exists...', e)

        metadata = extract_video_metadata(video.hash_value)
        interval = metadata['frame_rate']

        video_pipe = av.open(video.video_path)
        pass_count = 0
        arr = []
        for frame in video_pipe.decode(video=0):
            if pass_count % interval == 0:
                img = frame.to_image()
                arr.append(np.array(img))
            pass_count += 1

        mpq = multiprocessing.Queue()
        mpp = multiprocessing.Process(target=detect_person, args=(arr, mpq))
        mpp.start()
        mpp.join()
        ret = mpq.get()

        save_video_frame(metadata['hash_value'], arr, ret)
        feature_extract(case_video_path)
        video.is_detect_done = True
        video.save()

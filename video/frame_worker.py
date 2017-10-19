import os
import av
import skvideo.io
import numpy as np

from PIL import Image, ImageDraw

from video.models import Video, Person
from video.calculation import NumericStringParser
from object_detection.main import detect_person 


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
    video_obj.frame_rate = calculate_string_exp(video['video']['@avg_frame_rate'])
    video_obj.save()

    return metadata


def save_video_frame(hash_value, frames, bbox_list):
    idx = 0
    video = Video.objects.get(hash_value=hash_value)
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(video.video_path)),
        '%s_%s' % (
            video.hash_value,
            os.path.splitext(os.path.basename(video.video_path))[0]
        )
    )

    for frame_idx in range(len(frames)):
        origin_img = Image.fromarray(frames[frame_idx])
        draw = ImageDraw.Draw(origin_img)
        
        img_idx = 0

        for bbox, score in bbox_list[frame_idx]:
            person_name = os.path.join(
                file_path, 'bbox', '%d_%d.jpg' % (idx, img_idx)
            )
            feature_name = os.path.join(
                file_path, 'feat', '%d_%d.npy' % (idx, img_idx)
            )

            crop_img = origin_img.crop(bbox)
            crop_img.save(person_name)
            draw.rectangle(bbox, outline='red')

            img_idx += 1

            Person.objects.create(
                person_path=person_name,
                feature_path=feature_name,
                score=score,
                frame_num=video.frame_rate*frame_idx,
                time='2015-02-10T21:30',
                video=video,
            )
            origin_img.save(os.path.join(file_path, 'origin', '%d.jpg' % idx))
        idx += 1


def extract_video_frame_array(videos):
    for video in videos:
        file_path = video.video_path
        file_name = os.path.basename(file_path)
        folder_name = '%s_%s' % (video.hash_value, os.path.splitext(file_name)[0])
        folder_path = os.path.dirname(os.path.abspath(file_path))
        full_path = os.path.join(folder_path, folder_name)

        try:
            os.mkdir(full_path)
            os.mkdir(os.path.join(full_path, 'origin'))
            os.mkdir(os.path.join(full_path, 'bbox'))
            os.mkdir(os.path.join(full_path, 'feat'))
        except:
            print('Folder already exists..')
        
        metadata = extract_video_metadata(video.hash_value)
        interval = metadata['frame_rate']

        video_pipe = av.open(file_path)
        pass_count = 0
        arr = []
        for frame in video_pipe.decode(video=0):
            if pass_count % interval == 0:
                img = frame.to_image()
                arr.append(np.array(img))
            pass_count += 1
        ret = detect_person(arr)
        save_video_frame(metadata['hash_value'], arr, ret)
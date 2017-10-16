import os
import av
import skvideo.io
import numpy as np

from video.models import Video
from video.calculation import NumericStringParser
from object_detection.main import detect_person 


_NUM_STR_PARSER = NumericStringParser()


def calculate_string_exp(data):
    return round(_NUM_STR_PARSER.eval(data))


def extract_video_metadata(file_path):
    video = skvideo.io.ffprobe(file_path)
    video_obj = Video.objects.get(video_path=file_path)

    metadata = {
        'total_frame': int(video['video']['@nb_frames']),
        'frame_rate': calculate_string_exp(video['video']['@avg_frame_rate']),
    }

    video_obj.total_frame = int(video['video']['@nb_frames'])
    video_obj.frame_rate = calculate_string_exp(video['video']['@avg_frame_rate'])
    video_obj.save()

    return metadata


def extract_video_frame_array(file_list):
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        folder_path = os.path.dirname(os.path.abspath(file_path))

        '''
        try:
            os.mkdir(full_path)
        except:
            print('Folder already exists..')
        '''
        
        metadata = extract_video_metadata(file_path)
        interval = metadata['frame_rate']

        video = av.open(file_path)
        pass_count = 0
        for frame in video.decode(video=0):
            if pass_count % interval == 0:
                img = frame.to_image()
                arr = np.array(img)
                ret = detect_person(arr)
                print(ret)
            pass_count += 1


def extract_video_frame_image(file_path, interval=30):
    file_name = ''
    folder_path = ''
        
    try:
        os.mkdir(full_path)
    except:
       print('Folder already exists..')

    video = av.open(file_path)
    pass_count = 0
    for frame in video.decode(video=0):
        if pass_count % interval == 0:
            frame.to_image().save(
                folder_path + '/%d.jpeg' % frame.index
            )
        pass_count += 1


'''
if __name__ == '__main__':
    file_list = [
        #'/home/punk/data-picker/assets/test.mp4',
        '/home/punk/data-picker/assets/bmw.mp4',
    ]
    extract_video_frame_array(file_list)
    #extract_video_frame_image(file_path)
'''

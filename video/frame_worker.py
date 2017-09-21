import os
import av
import skvideo.io

from video.models import Video
from video.calculation import NumericStringParser


class FrameWorker:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self):
        self.running_time = 0
        self.frame = 0
        self.video = ''

    def extract_video_info(self, video):
        self.video = video
        metadata = skvideo.io.ffprobe(video)

        # fps
        self.frame = self.calculate_video_frame(
            metadata['video']['@r_frame_rate']
        )
        self.running_time = metadata['video']['@duration']    # duration

    def calculate_video_frame(self, data):
        num_str_parser = NumericStringParser()
        result = num_str_parser.eval(data)

        return result

    def extract_video_frame(self, video, interval):
        container = av.open(video)
        pass_count = 0

        folder_name = os.path.basename(video)
        full_path = self.BASE_DIR + '/' + folder_name
        
        try:
            os.mkdir(full_path)
        except:
            print('Folder already exists..')
        
        for frame in container.decode(video=0):
            if pass_count % interval == 0:
                frame.to_image().save(
                    full_path + '/img-%04d.jpeg' % frame.index
                )
            pass_count += 1

    def cut_video(self, video, start, end):
        pass

    def save_video_info(self, video):
        info = Video.objects.get(video=video)
        info.frame = self.frame
        info.running_time = self.running_time
        info.save()

    # for testing
    def extract_random_frame(self, video):
        pass

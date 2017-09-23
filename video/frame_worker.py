from __future__ import division
import os
import av
import skvideo.io

from video.models import Video
from video.calculation import NumericStringParser


class FrameWorker:
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ) + '/assets/'

    def __init__(self, *arg):
        if arg:
            self.video = arg[0]
        else:
            self.video = ''
        self.running_time = 0
        self.frame = 0

    def extract_video_info(self, *arg):
        if arg:
            self.video = arg[0]
        
        metadata = skvideo.io.ffprobe(self.video)

        # fps
        self.frame = self.calculate_video_frame(
            metadata['video']['@r_frame_rate']
        )
        self.running_time = metadata['video']['@duration']    # duration

    def calculate_video_frame(self, data):
        num_str_parser = NumericStringParser()
        result = num_str_parser.eval(data)

        return result

    def extract_video_frame(self, interval, *arg):
        if arg:
            self.video = arg[0]
        
        container = av.open(self.video)
        pass_count = 0

        folder_name = os.path.splitext(os.path.basename(self.video))[0]
        full_path = self.BASE_DIR + folder_name
        
        try:
            os.mkdir(full_path)
        except:
            print('Folder already exists..')

        for frame in container.decode(video=0):
            if pass_count % interval == 0:
                frame.to_image().save(
                    full_path + '/%d.jpeg' % frame.index
                )
            pass_count += 1

    def cut_video(self, start, end, *arg):
        pass

    def save_video_info(self, *arg):
        if arg:
            self.video = arg[0]
        '''
        info = Video.objects.get(video=self.video)
        info.frame = self.frame
        info.running_time = self.running_time
        info.save()
        '''
        Video.objects.create(
            video_path=self.video,
            frame=self.frame,
            running_time=self.running_time
        )

    # for testing
    def extract_random_frame(self, *arg):
        pass

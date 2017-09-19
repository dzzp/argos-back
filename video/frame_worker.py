import skvideo.io


class FrameWorker:
    def __init__(self):
        self.running_time = 0
        self.frame = 0

    def __init__(self, running_time, frame):
        self.running_time = running_time
        self.frame = frame

    def extract_video_info(self, video):
        metadata = skvideo.io.ffprobe(video)
        fps = metadata['video']['@r_frame_rate']
        duration_sec = metadata['video']['@duration']

        self.running_time = duration_sec
        self.frame = fps

    def extract_video_frame(self, video, interval):
        pass

    def cut_video(self, video, start, end):
        pass

    '''
    def save_video_info(self, video):
        pass
    '''

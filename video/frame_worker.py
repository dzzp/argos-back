

class FrameWorker:
    def __init__(self):
        self.running_time = '00:00:00.00'
        self.frame = 0

    def __init__(self, running_time, frame):
        self.running_time = running_time
        self.frame = frame

    def extract_video_info(self, video):
        pass

    def extract_video_frame(self, video, interval):
        pass

    def cut_video(self, video, start, end):
        pass

    '''
    def save_video_info(self, video):
        pass
    '''

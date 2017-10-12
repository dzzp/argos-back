import os
import av
import numpy as np


def extract_video_frame_array(file_path, interval=30):
    file_name = os.path.basename(file_path)
    folder_path = os.path.dirname(os.path.abspath(file_path))

    print(file_name)
    print(folder_path)
    '''
    try:
        os.mkdir(full_path)
    except:
        print('Folder already exists..')
    '''

    video = av.open(file_path)
    pass_count = 0
    for frame in video.decode(video=0):
        if pass_count % interval == 0:
            img = frame.to_image()
            arr = np.array(img)
            # using detect function...
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
    file_path = '/home/punk/data-picker/assets/test.mp4'
    extract_video_frame_array(file_path)
    #extract_video_frame_image(file_path)
'''

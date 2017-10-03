import os
import re
from django.forms import ValidationError


def file_validator(value):
    file_types = ('.mov', '.mp4', '.avi')
    file_ext = os.path.splitext(value)

    if file_ext[-1] in file_types:
        if is_video_exists(value):
            return True
    
    return False

def is_video_exists(value):
    if os.path.isfile(value):
        return True
    else:
        return False

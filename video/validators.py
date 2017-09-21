import os
import re
from django.forms import ValidationError


def lnglat_validator(value):
    if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
        raise ValidationError('Invalid Lng, Lat Type')


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

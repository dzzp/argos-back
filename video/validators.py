import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_ext = [
        '.avi',
        '.mpg',
        '.mpeg',
        '.wmv',
        '.mp4',
        '.mov',
    ]

    if not ext.lower() in valid_ext:
        raise ValidationError('Unsupoorted file extension')

import os

from django.shortcuts import render
from video.models import Video
from video.validators import file_validator

def main_view(request):
    return render(request, 'main.html')


def upload_path_view(request):
    error = None
    if request.method == 'POST':
        # Checking file type
        if  file_validator(request.POST['file-path']):
            try:
                Video.objects.create(
                    video_path=request.POST['file-path'],
                )
            except:
                error = {'error': '[ERROR] File already exists'}
        else:
            error = {'error': '[ERROR] File type error'}

    return render(request, 'upload_path.html', error)


def load_project_view(request):
    return render(request, 'base.html')

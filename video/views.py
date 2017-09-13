import os

from django.shortcuts import render
from video.models import Video


def main_view(request):
    return render(request, 'main.html')


def upload_path_view(request):
    if request.method == 'POST':
        file_types = ('.mov', '.mp4', '.avi')
        file_ext = os.path.splitext(request.POST['file-path'])
        if file_ext[-1] in file_types:
            Video.objects.create(
                video_path=request.POST['file-path'],
            )

    return render(request, 'upload_path.html')


def load_project_view(request):
    return render(request, 'base.html')

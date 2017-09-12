from django.shortcuts import render


def main_view(request):
    return render(request, 'main.html')


def upload_path_view(request):
    return render(request, 'base.html')


def load_project_view(request):
    return render(request, 'base.html')

"""data_picker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from video.views import main_view, upload_path_view, load_project_view

urlpatterns = [
    url(r'^$', main_view, name='main'),
    url(r'^upload_path/$', upload_path_view, name='upload_path'),
    url(r'^load_project/$', load_project_view, name='load'),
    url(r'^admin/', admin.site.urls),
]

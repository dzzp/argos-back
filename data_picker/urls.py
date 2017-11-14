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

from video import views


urlpatterns = [
    url(r'^cases/$', views.cases, name='cases'),
    url(r'^cases/([a-z0-9]{7})/videos/$', views.cases_hash_videos, name='cases_hash_videos'),
    url(r'^cases/([a-z0-9]{7})/videos/([a-z0-9]{7})/$', views.cases_hash_videos_hash, name='cases_hash_videos_hash'),
    url(r'^cases/([a-z0-9]{7})/probes/$', views.cases_hash_probes, name='cases_hash_probes'),
    url(r'^cases/([a-z0-9]{7})/galleries/$', views.cases_hash_galleries, name='cases_hash_galleries'),
    url(r'^cases/([a-z0-9]{7})/processing/$', views.processing, name='processing'),
    url(r'^admin/', admin.site.urls),
]

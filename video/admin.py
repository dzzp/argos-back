from django.contrib import admin
from video.models import Video, TestVideo


class VideoAdmin(admin.ModelAdmin):
    list_display = ('_id', 'video_path', 'time', 'lat', 'lng',)


class TestVideoAdmin(admin.ModelAdmin):
    list_display = ('video',)

admin.site.register(Video, VideoAdmin)
admin.site.register(TestVideo, TestVideoAdmin)

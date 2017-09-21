from django.contrib import admin
from video.models import Video, SubVideo, DataSet, TestVideo


class VideoAdmin(admin.ModelAdmin):
    list_display = ('_id', 'video_path', 'running_time')


class SubVideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'location', 'time')


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('_id', 'video', 'coordinate', 'time')

class TestVideoAdmin(admin.ModelAdmin):
    list_display = ('video',)

admin.site.register(Video, VideoAdmin)
admin.site.register(SubVideo, SubVideoAdmin)
admin.site.register(DataSet, DataSetAdmin)

admin.site.register(TestVideo, TestVideoAdmin)

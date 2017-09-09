from django.contrib import admin
from video.models import Video, DataSet


class VideoAdmin(admin.ModelAdmin):
    list_display = ('_id', 'video', 'running_time')


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('_id', 'video', 'coordinate', 'time')


admin.site.register(Video, VideoAdmin)
admin.site.register(DataSet, DataSetAdmin)

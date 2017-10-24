from django.contrib import admin
from video.models import Video, Person, TestVideo, LoadList


class VideoAdmin(admin.ModelAdmin):
    list_display = (
        '_id',
        'video_path',
        'memo',
        'lat',
        'lng',
        'time',
        'frame_rate',
        'total_frame',
        'hash_value',
    )


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        '_id',
        'video',
        'person_path',
        'feature_path',
        'score',
        'frame_num',
        'time',
    )


class TestVideoAdmin(admin.ModelAdmin):
    list_display = ('video',)


class LoadListAdmin(admin.ModelAdmin):
    list_display = ('video', 'current', 'total',)


admin.site.register(Video, VideoAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(TestVideo, TestVideoAdmin)

admin.site.register(LoadList, LoadListAdmin)

from django.contrib import admin
from video.models import (
    Case, Video, Person,
    ProbeList, LoadList, TestVideo,
)


class CaseAdmin(admin.ModelAdmin):
    list_display = (
        '_id',
        'case_title',
        'group_hash_id',
        'generated_datetime',
        'memo',
    )


class VideoAdmin(admin.ModelAdmin):
    list_display = (
        '_id',
        'video_path',
        'memo',
        'lat',
        'lng',
        'date',
        'time',
        'frame_rate',
        'total_frame',
        'hash_value',
        'is_detect_done',
    )


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        '_id',
        'video',
        'hash_value',
        'person_path',
        'score',
        'frame_num',
        'shot_time',
    )


class ProbeListAdmin(admin.ModelAdmin):
    list_display = ('case', 'person',)


class LoadListAdmin(admin.ModelAdmin):
    list_display = ('case', 'current', 'total',)


class TestVideoAdmin(admin.ModelAdmin):
    list_display = ('video',)


admin.site.register(Case, CaseAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(ProbeList, ProbeListAdmin)
admin.site.register(LoadList, LoadListAdmin)
admin.site.register(TestVideo, TestVideoAdmin)

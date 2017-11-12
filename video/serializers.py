from video.models import Person


class PersonSerializer:
    _video = None
    _person_list = None

    def __init__(self, person_data):
        self._person_list = dict()

        for person in person_data:
            if not person['shot_time'] in self._person_list:
                self._person_list[person['shot_time']] = list()
            else:
                self._person_list[person['shot_time']].append(
                    Person.objects.create(
                        video=person['video'],
                        person_path=person['person_path'],
                        score=person['score'],
                        frame_num=person['frame_num'],
                        shot_time=person['shot_time'],
                    )
                )

        self._video = person['video']

    def getPersonList(self):
        video = dict()

        video['lat'] = self._video.lat
        video['lng'] = self._video.lng
        video['path'] = self._video.video_path
        video['memo'] = self._video.memo
        video['imgs'] = []
        for time in self._person_list:
            if len(Person.objects.filter(shot_time=time)) > 0:
                img = dict()
                img['persons'] = list()
                for person in self._person_list[time]:
                    data = {
                        'bbox_img': person.person_path,
                        'person_idx': person.hash_value
                    }

                    img['persons'].append(data)
                img['time'] = str(time)
                video['imgs'].append(img)
        return video

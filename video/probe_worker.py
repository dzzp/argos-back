import numpy as np

from PIL import Image


def executing_probe(person_list):
    for person_hash in person_list:
        person = Person.objects.get(hash_value=person_hash)
        img = Image.open(person.person_path)
        #feature = 

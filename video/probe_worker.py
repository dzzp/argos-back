import os
import subprocess
import numpy as np

from PIL import Image
from glob import glob
from django.conf import settings
from video.models import Person

_BATCH_SIZE = 50

_BASE_DIR = '/home/dzzp/Desktop/argos-back/'

_CAFFE_PATH = '/home/dzzp/Desktop/caffe/'
_CAFFE_CMD = os.path.join(_CAFFE_PATH, 'build/tools/extract_features')

_SPINDLE_PATH = os.path.join(settings.BASE_DIR, 'SpindleNet')
_SPINDLE_MODEL = os.path.join(_SPINDLE_PATH, 'spindlenet_iter_50000.caffemodel')

_RPN_PATH = os.path.join(_BASE_DIR, 'RPN')
#_RPN_PATH = os.path.join(setttings._BASE_DIR, 'RPN')
_RPN_INF_CMD = 'python ' + _RPN_PATH + '/inference.py'
_RPN_PROTO_PATH = os.path.join(_RPN_PATH, 'spindlenet_test.prototxt')

_CONVERT_CMD = 'python ' + _RPN_PATH + '/convert_lmdb_to_numpy.py'


def feature_extract(video_path):
    after_rpn = 'after_rpn.txt'
    feature_path = os.path.join(video_path, 'feat', 'features.npy')

    with open('file_list.txt', 'w') as f:
        f_names = glob(os.path.join(video_path, 'bbox', '*'))
        iter_len = (len(f_names) + _BATCH_SIZE - 1) // _BATCH_SIZE
        for f_name in f_names:
            f.write('%s 0\n' % f_name)

    subprocess.call(_RPN_INF_CMD + ' file_list.txt ' + after_rpn, shell=True)
    subprocess.call(
        '{caffe_cmd} {spindle_model} {rpn_proto} fc7/spindle,label {feature_lmdb},{label_lmdb} {iter_len} lmdb GPU 0'.format(
              caffe_cmd=_CAFFE_CMD,
              spindle_model=_SPINDLE_MODEL,
              rpn_proto= _RPN_PROTO_PATH,
              feature_lmdb=os.path.join(_RPN_PATH, 'features_lmdb'),
              label_lmdb=os.path.join(_RPN_PATH, 'label_lmdb'),
              iter_len=iter_len
        ), shell=True
    )

    subprocess.call(
        '{convert_cmd} {feature_lmdb} {feature_path}'.format(
            convert_cmd=_CONVERT_CMD,
            feature_lmdb=os.path.join(_RPN_PATH, 'features_lmdb'),
            feature_path=feature_path
        ), shell=True
    )
    subprocess.call(
        'rm -rf {feature_lmdb}'.format(
            feature_lmdb=os.path.join(_RPN_PATH, 'features_lmdb')
        ), shell=True
    )
    subprocess.call(
        'rm -rf {label_lmdb}'.format(
            label_lmdb=os.path.join(_RPN_PATH, 'label_lmdb')
        ), shell=True
    )

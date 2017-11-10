import os


_BASE_DIR = '/home/dzzp/Desktop/argos-back'
_CAFFE_PATH = '/home/dzzp/Desktop/caffe/python/'


def config():
    param = {}

    param['use_gpu'] = 0

    param['caffe_model'] = os.path.join(
        _BASE_DIR, '/RPN/model/pose_iter_265000.caffemodel'
    )
    param['deploy_file'] = os.path.join(
        _BASE_DIR, '/RPN/model/pose_deploy.prototxt'
    )

    param['box_size'] = 256
    param['pad_value'] = 128
    param['magic'] = 0.2
    param['sigma'] = 21
    param['caffe_path'] = _CAFFE_PATH
    param['map_layer_name'] = 'Mconv5_stage3'

    return param

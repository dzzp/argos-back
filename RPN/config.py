def config():
  param = {}
  param['use_gpu'] = 0
  param['caffe_model'] = '/home/dzzp/Desktop/argos-back/RPN/model/pose_iter_265000.caffemodel'
  param['deploy_file'] = '/home/dzzp/Desktop/argos-back/RPN/model/pose_deploy.prototxt'
  param['box_size'] = 256
  param['pad_value'] = 128
  param['magic'] = 0.2
  param['sigma'] = 21
  param['caffe_path'] = '/home/dzzp/Desktop/caffe/python/'
  param['map_layer_name'] = 'Mconv5_stage3'
  return param


# ARGOS-BACK

argos-back for [argos-front](https://github.com/dzzp/argos-front)

## Environments

- Ubuntu 16.04+
- Python2 & 3
- FFmpeg
- OpenCV
- Caffe _[(custom)](https://github.com/dzzp/caffe)_
- **[SpindleNet](https://github.com/dzzp/SpindleNet) pre-trained model**

## Requirements

[NEED TO CHECK DETAILS](https://github.com/dzzp/argos-back/blob/master/APT_PKG)

- django
- tensorflow
- numpy
- scikit-image
- scikit-video

_and more libraries.._

## Object detection model

You need to download a object detection model from [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)

**object_detection/main.py**

```python
...
MODEL_NAME = os.path.join(
    settings.BASE_DIR,
    'object_detection/faster_rcnn_resnet101_coco_2017_11_08',    # HERE!
)
...
```

## API Documentation

[HERE](https://github.com/dzzp/argos-api)

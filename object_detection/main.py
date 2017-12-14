import os
import numpy
import tensorflow as tf

from PIL import Image
from io import StringIO
from django.conf import settings
from collections import defaultdict

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# Need to download a object detection model
MODEL_NAME = os.path.join(
    settings.BASE_DIR,
    'object_detection/faster_rcnn_resnet101_coco_2017_11_08',
)

# Path to frozen detection graph.
# This is the actual model that is used for the object detection.
PATH_TO_CKPT = os.path.join(MODEL_NAME, 'frozen_inference_graph.pb')


def detect_person(images, queue):
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            ret = []

            for image in images:
                img_ret = []
                image_np = numpy.expand_dims(image, axis=0)
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np}
                )

                boxes = numpy.squeeze(boxes)
                scores = numpy.squeeze(scores)
                classes = numpy.squeeze(classes).astype(numpy.int32)

                for i in range(int(num[0])):
                    if float(scores[i]) >= 0.95 and classes[i] == 1:
                        ymin = numpy.clip(int(boxes[i][0]*image.shape[0]), 0, image.shape[0]-1)
                        xmin = numpy.clip(int(boxes[i][1]*image.shape[1]), 0, image.shape[1]-1)
                        ymax = numpy.clip(int(boxes[i][2]*image.shape[0]), 0, image.shape[0]-1)
                        xmax = numpy.clip(int(boxes[i][3]*image.shape[1]), 0, image.shape[1]-1)
                        img_ret.append(([xmin, ymin, xmax, ymax], scores[i]))
                ret.append(img_ret)
    tf.reset_default_graph()
    queue.put(ret)

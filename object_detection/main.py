import glob
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import time
import zipfile

from django.conf import settings
from collections import defaultdict
from io import StringIO
from PIL import Image

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# What model to download.
#MODEL_NAME = settings.BASE_DIR + '/object_detection/ssd_mobilenet_v1_coco_11_06_2017'
MODEL_NAME = settings.BASE_DIR + '/object_detection/faster_rcnn_resnet101_coco_11_06_2017'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = os.path.join(MODEL_NAME, 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(settings.BASE_DIR + '/object_detection/data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def detect_person(images):
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
                image_np = np.expand_dims(image, axis=0)
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np}
                )

                boxes = np.squeeze(boxes)
                scores = np.squeeze(scores)
                classes = np.squeeze(classes).astype(np.int32)

                for i in range(int(num[0])):
                    if float(scores[i]) >= 0.95 and classes[i] == 1:
                        ymin = np.clip(int(boxes[i][0] * image.shape[0]), 0, image.shape[0] - 1)
                        xmin = np.clip(int(boxes[i][1] * image.shape[1]), 0, image.shape[1] - 1)
                        ymax = np.clip(int(boxes[i][2] * image.shape[0]), 0, image.shape[0] - 1)
                        xmax = np.clip(int(boxes[i][3] * image.shape[1]), 0, image.shape[1] - 1)
                        #Image.fromarray(image[ymin:ymax, xmin:xmax]).save('/home/dzzp/Desktop/asdf/qqqq%d-%f-%d-%d-%d-%d.jpg' % (len(ret), scores[i], xmin, ymin, xmax, ymax))
                        #ret.append(image[ymin:ymax, xmin:xmax])
                        img_ret.append(([xmin, ymin, xmax, ymax], scores[i]))
                ret.append(img_ret)
            return ret

from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
# from object_detection.pepper_detection import django #import django/pepper/detection/object_detection/pepper_detection/django.py
import numpy as np
import tensorflow as tf
import datetime
import io
from PIL import Image

from attmgt.models import Attendance
from attmgt.models import ImageFile

#MODEL_NAME = '/home/cc/pepper/django/pepper/detection/object_detection/pepper_detection/ssd_mobilenet_v1_coco_11_06_2017'
MODEL_NAME='detection/object_detection/ssd_mobilenet_v1_coco_11_06_2017/'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = 'detection/object_detection/data/mscoco_label_map.pbtxt' #os.path.join('data', 'mscoco_label_map.pbtxt')
from detection.object_detection.utils import label_map_util
from detection.object_detection.utils import visualization_utils as vis_util


NUM_CLASSES = 90

IMAGE_SIZE = (12, 8)

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


@require_POST
@csrf_exempt
def detect_received_image(request):
    uploaded_image = request.FILES["image"]
    x, y = uploaded_image.name.split('_')[1].split('-')
    y = y.rsplit('.', 1)[0]
    # imagefile = ImageFile(x=float(x), y=float(y), image=uploaded_image)
    # imagefile.save()

    # img_bin = io.BytesIO(image) # メモリに保存してディレクトリ偽装のように(PIL読み込みのため)
    pil_img = Image.open(uploaded_image)
    image_np = load_image_into_numpy_array(pil_img)
    result_flg, result_np = detect_object(image_np)
    att = Attendance(student_id=0, att=result_flg)
    att.save()

    img = Image.fromarray(result_np)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    pillow_image = ContentFile(buf.getvalue())
    result_image = InMemoryUploadedFile(pillow_image,
                                        None,
                                        uploaded_image.name,
                                        'image/png',
                                        pillow_image.tell(),
                                        None)
    # request.FILES["image"] = result_image
    # result_image = request.FILES["image"]
    imagefile = ImageFile(x=float(x), y=float(y), image=result_image)
    imagefile.save()

    # print(request)
    return HttpResponse()


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


def detect_object(image_np): #detect picture basic function
    #sess=tf.Session(graph=detection_graph)
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    with sess:
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
        boxes=np.squeeze(boxes)
        classes=np.squeeze(classes).astype(np.int32)
        scores=np.squeeze(scores)
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8)
    print(classes[0])
    if 1 in classes[:10]:
        return True, image_np
    else:
        return False, image_np
    #return image_np,boxes,classes,scores #return image and detect object class and score

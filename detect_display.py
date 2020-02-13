# pylessons
import time
import mss
from datetime import datetime
from multiprocessing import Pipe
import multiprocessing
from yolo3.utils import image_preporcess
from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
from keras.layers import Input
from keras.models import load_model
from keras import backend as K
import numpy as np
import cv2
import colorsys
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'


# set start time to current time
start_time = time.time()
# displays the frame rate every 2 second
display_time = 2
# Set primarry FPS to 0
fps = 0

start_time = time.time()
display_time = 2  # displays the frame rate every 2 second
fps = 0
sct = mss.mss()
# Set monitor size to capture
videoWidth = 720
videoHeight = 720

originx = 240
originy = 40

modelDir = "D:\Projects Data\AI\AdTracker\Model\\42_Ads"
modelName = "\\42_Ads"

monitor = {"top": originy, "left": originx, "width": originx +
           videoWidth, "height": originy+videoHeight}


class YOLO(object):
    _defaults = {
        "model_path": modelDir+modelName+"_last.h5",
        "anchors_path": modelDir+modelName+"_anchors.txt",
        "classes_path": modelDir+modelName+".names",
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "text_size": 3,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)  # set up default values
        self.__dict__.update(kwargs)  # and update with user overrides
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.boxes, self.scores, self.classes = self.generate()

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith(
            '.h5'), 'Keras model or weights must be a .h5 file.'

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        is_tiny_version = num_anchors == 6  # default setting
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            self.yolo_model = tiny_yolo_body(Input(shape=(None, None, 3)), num_anchors//2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None, None, 3)), num_anchors//3, num_classes)
            # make sure model, anchors and classes match
            self.yolo_model.load_weights(self.model_path)
        else:
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        print('{} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))

        # Shuffle colors to decorrelate adjacent classes.
        np.random.shuffle(self.colors)

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2, ))
        boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                                           len(self.class_names), self.input_image_shape,
                                           score_threshold=self.score, iou_threshold=self.iou)
        return boxes, scores, classes

    def detect_image(self, image):
        if self.model_image_size != (None, None):
            assert self.model_image_size[0] % 32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1] % 32 == 0, 'Multiples of 32 required'
            boxed_image = image_preporcess(
                np.copy(image), tuple(reversed(self.model_image_size)))
            image_data = boxed_image

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                # [image.size[1], image.size[0]],
                self.input_image_shape: [image.shape[0], image.shape[1]],
                K.learning_phase(): 0
            })
        # print('Found {} boxes for {}'.format(len(out_boxes), 'img'))

        thickness = (image.shape[0] + image.shape[1]) // 600
        fontScale = 1
        ObjectsList = []

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            label = '{} {:.2f}'.format(predicted_class, score)
            # label = '{}'.format(predicted_class)
            scores = '{:.2f}'.format(score)

            print("\t\t\t"+predicted_class+" " +
                  str(float(float(scores)*100))+" "+str(datetime.now()))

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.shape[0], np.floor(
                bottom + 0.5).astype('int32'))
            right = min(image.shape[1], np.floor(right + 0.5).astype('int32'))

            mid_h = (bottom-top)/2+top
            mid_v = (right-left)/2+left

            # put object rectangle
            cv2.rectangle(image, (left, top), (right, bottom),
                          self.colors[c], thickness)

            # get text size
            (test_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, thickness/self.text_size, 1)

            # put text rectangleqq
            cv2.rectangle(image, (left, top), (left + test_width, top -
                                               text_height - baseline), self.colors[c], thickness=cv2.FILLED)

            # put text above rectangle
            cv2.putText(image, label, (left, top-2), cv2.FONT_HERSHEY_SIMPLEX,
                        thickness/self.text_size, (0, 0, 0), 1)

            # add everything to list
            ObjectsList.append(
                [top, left, bottom, right, mid_v, mid_h, label, scores])

        return image, ObjectsList

    def close_session(self):
        self.sess.close()

    def detect_img(self, image):
        # image = cv2.imread(image, cv2.IMREAD_COLOR)
        original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        original_image_color = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        r_image, ObjectsList = self.detect_image(original_image_color)
        return r_image, ObjectsList


def GRABMSS_screen(p_input):
    while True:
        # Grab screen image
        img = np.array(sct.grab(monitor))

        # Put image from pipe
        p_input.send(img)


def SHOWMSS_screen(p_output):
    global fps, start_time
    yolo = YOLO()
    while True:
        img = p_output.recv()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        r_image, ObjectsList = yolo.detect_image(img)

        cv2.imshow("YOLO v3", r_image)
        fps += 1
        TIME = time.time() - start_time
        if (TIME) >= display_time:
            print("FPS: ", fps / (TIME))
            fps = 0
            start_time = time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    yolo.close_session()


if __name__ == "__main__":
    p_output, p_input = Pipe()

    # creating new processes
    p1 = multiprocessing.Process(target=GRABMSS_screen, args=(p_input,))
    p2 = multiprocessing.Process(target=SHOWMSS_screen, args=(p_output,))

    # starting our processes
    p1.start()
    p2.start()


# # import the necessary packages
# import numpy as np
# import argparse
# import imutils
# import time
# import cv2
# import os
# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--input", required=True,
#                 help="path to input video")
# ap.add_argument("-o", "--output", required=True,
#                 help="path to output video")
# ap.add_argument("-y", "--yolo", required=True,
#                 help="base path to YOLO directory")
# ap.add_argument("-c", "--confidence", type=float, default=0.5,
#                 help="minimum probability to filter weak detections")
# ap.add_argument("-t", "--threshold", type=float, default=0.3,
#                 help="threshold when applyong non-maxima suppression")
# args = vars(ap.parse_args())

# # load the COCO class labels our YOLO model was trained on
# labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
# LABELS = open(labelsPath).read().strip().split("n")
# # initialize a list of colors to represent each possible class label
# np.random.seed(42)
# COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
#                            dtype="uint8")
# # derive the paths to the YOLO weights and model configuration
# weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
# configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])
# # load our YOLO object detector trained on COCO dataset (80 classes)
# # and determine only the *output* layer names that we need from YOLO
# print("[INFO] loading YOLO from disk...")
# net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
# ln = net.getLayerNames()
# ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# # initialize the video stream, pointer to output video file, and
# # frame dimensions
# vs = cv2.VideoCapture(args["input"])
# writer = None
# (W, H) = (None, None)
# # try to determine the total number of frames in the video file
# try:
#     prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2()
#     else cv2.CAP_PROP_FRAME_COUNT
#     total = int(vs.get(prop))
#     print("[INFO] {} total frames in video".format(total))
# # an error occurred while trying to determine the total
# # number of frames in the video file
# except:
#     print("[INFO] could not determine # of frames in video")
#     print("[INFO] no approx. completion time can be provided")
#     total = -1

# # loop over frames from the video file stream
# while True:
#     # read the next frame from the file
#     (grabbed, frame) = vs.read()
#     # if the frame was not grabbed, then we have reached the end
#     # of the stream
#     if not grabbed:
#         break
#     # if the frame dimensions are empty, grab them
#     if W is None or H is None:
#         (H, W) = frame.shape[:2]
#     # construct a blob from the input frame and then perform a forward
#     # pass of the YOLO object detector, giving us our bounding boxes
#     # and associated probabilities
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
#                                  swapRB=True, crop=False)
#     net.setInput(blob)
#     start = time.time()
#     layerOutputs = net.forward(ln)
#     end = time.time()
#     # initialize our lists of detected bounding boxes, confidences,
#     # and class IDs, respectively
#     boxes = []
#     confidences = []
#     classIDs = []
#     # loop over each of the layer outputs
#     for output in layerOutputs:
#         # loop over each of the detections
#         for detection in output:
#             # extract the class ID and confidence (i.e., probability)
#             # of the current object detection
#             scores = detection[5:]
#             classID = np.argmax(scores)
#             confidence = scores[classID]
#             # filter out weak predictions by ensuring the detected
#             # probability is greater than the minimum probability
#             if confidence > args["confidence"]:
#                 # scale the bounding box coordinates back relative to
#                 # the size of the image, keeping in mind that YOLO
#                 # actually returns the center (x, y)-coordinates of
#                 # the bounding box followed by the boxes' width and
#                 # height
#                 box = detection[0:4] * np.array([W, H, W, H])
#                 (centerX, centerY, width, height) = box.astype("int")
#                 # use the center (x, y)-coordinates to derive the top
#                 # and and left corner of the bounding box
#                 x = int(centerX - (width / 2))
#                 y = int(centerY - (height / 2))
#                 # update our list of bounding box coordinates,
#                 # confidences, and class IDs
#                 boxes.append([x, y, int(width), int(height)])
#                 confidences.append(float(confidence))
#                 classIDs.append(classID)
#     # apply non-maxima suppression to suppress weak, overlapping
#     # bounding boxes
#     idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
#                             args["threshold"])
#     # ensure at least one detection exists
#     if len(idxs) > 0:
#         # loop over the indexes we are keeping
#         for i in idxs.flatten():
#             # extract the bounding box coordinates
#             (x, y) = (boxes[i][0], boxes[i][1])
#             (w, h) = (boxes[i][2], boxes[i][3])
#             # draw a bounding box rectangle and label on the frame
#             color = [int(c) for c in COLORS[classIDs[i]]]
#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#             text = "{}: {:.4f}".format(LABELS[classIDs[i]],
#                                        confidences[i])
#             cv2.putText(frame, text, (x, y - 5),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#     # check if the video writer is None
#     if writer is None:
#         # initialize our video writer
#         fourcc = cv2.VideoWriter_fourcc(*"MJPG")
#         writer = cv2.VideoWriter(args["output"], fourcc, 30,
#                                  (frame.shape[1], frame.shape[0]), True)
#         # some information on processing single frame
#         if total > 0:
#             elap = (end - start)
#             print("[INFO] single frame took {:.4f} seconds".format(elap))
#             print("[INFO] estimated total time to finish: {:.4f}".format(
#                 elap * total))
#     # write the output frame to disk
#     writer.write(frame)
# # release the file pointers
# print("[INFO] cleaning up...")
# writer.release()
# vs.release()

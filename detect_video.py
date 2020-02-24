import cv2
import csv
import time
import numpy as np
from datetime import timedelta

csvFilePath = "/home/harsh/Desktop/"
videoPath = "/mnt/6C8CA6790B328288/Projects/AI/AdTracker/Test Videos/test.mp4"
modelDir = "/mnt/6C8CA6790B328288/Projects/AI/AdTracker/Model"
modelName = "/9_Ads"
classesPath = modelDir+modelName+modelName+".names"
weightsPath = modelDir+modelName+modelName+".weights"
configPath = modelDir+modelName+modelName+".cfg"
frameH = 416
frameW = 416
thresholdConfidence = 0.5
thresholdNMS = 0.3


def init():
    pass


def captureFrames(path):

    # Load model
    classes = open(classesPath).read().strip().split("\n")
    np.random.seed(42)
    colors = np.random.randint(
        0, 255, size=(len(classes), 3), dtype="uint8")
    print("[INFO] Loading model...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    # take video feed
    videoObject = cv2.VideoCapture(path)
    (W, H) = (None, None)
    try:
        prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() else cv2.CAP_PROP_FRAME_COUNT
        total = int(videoObject.get(prop))
        print("Total Frames: {}".format(total))
    except:
        print("Error in reading file")
        total = -1
    frameIndex = 0
    while True:
        (grabbed, frame) = videoObject.read()

        if not grabbed:  # end of video
            break

        if W is None or H is None:
            (H, W) = frame.shape[:2]

        ln = net.getLayerNames()
        ln = [ln[i[0]-1] for i in net.getUnconnectedOutLayers()]
        blob = cv2.dnn.blobFromImage(
            frame, 1/255.0, (frameH, frameW), swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()
        fps = 1/(end-start)
        # print("[INFO] Took {:.6f} seconds, fps: {:.6f}".format(end-start, fps))

        # visualize results
        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > thresholdConfidence:
                    box = detection[0:4]*np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    x = int(centerX-(width/2))
                    y = int(centerY-(height/2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(
            boxes, confidences, thresholdConfidence, thresholdNMS)

        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][1], boxes[i][3])

                color = [int(c) for c in colors[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                text = "{}".format(classes[classIDs[i]])
                cv2.putText(frame, text, (x, y-5),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 2)

                calTime = timedelta(
                    seconds=frameIndex/25)

                print(frameIndex, " ", calTime, " ", classes[classIDs[i]])

                row = [frameIndex, calTime, classes[classIDs[i]]]
                updateCSV(row)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frameIndex += 1

    videoObject.release()
    cv2.destroyAllWindows()


def updateCSV(row):
    with open(csvFilePath+'adtrack.csv', mode='a', newline='') as csvFile:
        fileWriter = csv.writer(csvFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(row)


if __name__ == "__main__":
    init()
    captureFrames(videoPath)
    # runDetection(frame)  will be used after implementing pipelines

import cv2
import time
import numpy as np

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
    videoObject = cv2.VideoCapture(path)
    frameIndex = 0
    success = 1
    # while success:
    success, frame = videoObject.read()
    # frameIndex += 1
    runDetection(frame, frameIndex)


def runDetection(frame, frameIndex):
    (H, W) = frame.shape[:2]
    classes = open(classesPath).read().strip().split("\n")
    np.random.seed(42)
    colors = np.random.randint(
        0, 255, size=(len(classes), 3), dtype="uint8")
    print("[INFO] Loading model...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    ln = net.getLayerNames()
    ln = [ln[i[0]-1] for i in net.getUnconnectedOutLayers()]
    blob = cv2.dnn.blobFromImage(
        frame, 1/255.0, (frameH, frameW), swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    print("[INFO] YOLO took {:.6f} seconds".format(end-start))

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
            print(frameIndex, " ", classes[classIDs[i]], " ")
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)


if __name__ == "__main__":
    init()
    captureFrames(videoPath)
    # runDetection(frame)  will be used after implementing pipelines

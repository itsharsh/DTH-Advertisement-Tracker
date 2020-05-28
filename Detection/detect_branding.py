import os
import cv2
import sys
import time
import imutils
import platform
import numpy as np
from datetime import timedelta

import Detection
import path_config
from DB import update_db as DB

adTrackerDir = path_config.adTrackerDir
modelDir = path_config.modelDir
modelName = path_config.brandingModelName
originalVideoDir = path_config.originalVideoDir
processedVideoDir = path_config.processedVideoDir
detectionProcessedVideoDir = path_config.detectionProcessedVideoDir


configPath = path_config.brandingModelConfigPath
classesPath = path_config.brandingModelClassesPath
weightsPath = path_config.brandingModelWeightsPath

miscInfo = {
    "channelName": "Star Sports 1",
    "videoName": "20200117-213035.mp4",
    "adType": "Branding",
    "videoFPS": 25,
    "frameToRead": 1    # read every nth frame
}

frameH = 352
frameW = 352
thresholdNMS = 0.3
thresholdConfidence = 0.5


def init():
    pass


def loadModel():
    classes = open(classesPath).read().strip().split("\n")
    np.random.seed(len(classes))
    colors = np.random.randint(
        0, 255, size=(len(classes), 3), dtype="uint8")
    print("[INFO] Loading model...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    ln = net.getLayerNames()
    ln = [ln[i[0]-1] for i in net.getUnconnectedOutLayers()]
    return classes, colors, net, ln


def captureFrames(videoName):
    baseTimestamp = Detection.getTimestampFromVideofile(videoName)
    classes, colors, net, ln = loadModel()

    videoRead = cv2.VideoCapture(os.path.join(
        originalVideoDir, miscInfo["channelName"], videoName))
    # (W, H) = frame.shape[:2]
    (W, H) = (int(videoRead.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(videoRead.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    makeDirectoryCommand = "mkdir -p \"{}\"".format(os.path.join(detectionProcessedVideoDir,
                                              miscInfo["channelName"]))
    os.system(makeDirectoryCommand)
    videoWrite = cv2.VideoWriter(os.path.join(detectionProcessedVideoDir,
                                              miscInfo["channelName"], videoName), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), miscInfo["videoFPS"], (W, H))
    try:
        prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() else cv2.CAP_PROP_FRAME_COUNT
        total = int(videoRead.get(prop))
        print("Total Frames: {}".format(total))
    except:
        print("Exception while calculating total frames: ", sys.exc_info()[0])
        total = -1

    frameIndex = 0
    classIndex = [None]*len(classes)
    # classIndex = [[54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 184, 185, 185, 186, 186, 187, 187, 188, 188, 189, 189, 190, 190, 191, 191, 192, 192, 193, 193, 194, 194, 195, 195, 196, 196, 197, 197, 198, 198, 199, 199, 200, 200, 201, 201, 202, 202, 203, 203, 204, 204, 205, 205, 206, 206, 207, 207, 208, 208, 209, 209, 210, 210, 211, 211, 212, 212, 213, 213, 214, 214, 215, 215, 216, 216, 217, 217, 218, 218, 219, 219, 220, 220, 221, 221, 222, 222, 223, 223, 224, 224, 225, 225, 226, 226, 227, 227, 228, 228, 229, 229, 230, 230, 231, 231, 232, 232, 233, 233, 234, 234, 235, 235, 236, 236, 237, 237, 238, 238, 239, 239, 240, 240, 241, 241, 242, 242, 243, 243, 244, 244, 245, 245, 246, 246, 247, 247, 248, 248, 249, 249, 250, 250, 251, 251, 252, 252, 253, 253, 254, 254, 255, 255, 256, 256, 257, 257, 258, 258, 259, 259, 260, 260, 261, 261, 262, 262, 263, 263, 264, 264, 265,
    #                265, 266, 266, 267, 267, 268, 268], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], None, [184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 239, 240, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268], [156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183], [156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183], [156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182], [156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183], [156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183]]
    # Detection

    while True:
        (grabbed, frame) = videoRead.read()
        if not grabbed:  # end of video
            break

        frameTime = timedelta(
            seconds=frameIndex/miscInfo["videoFPS"])

        cv2.putText(frame, (baseTimestamp+frameTime).strftime("%Y/%m/%d-%H:%M:%S.%f")[:-3], (10, 30),
                    cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 1)

        blob = cv2.dnn.blobFromImage(
            frame, 1/255.0, (frameH, frameW), swapRB=True, crop=False)
        net.setInput(blob)

        if frameIndex % miscInfo["frameToRead"] == 0:
            start = time.time()
            layerOutputs = net.forward(ln)
            end = time.time()
            try:
                fps = miscInfo["frameToRead"]/(end-start)
            except ZeroDivisionError:
                fps = 0

            print("\t\t\t\t\t[INFO] [{}]One frame time: {:.6f} seconds, FPS: {:.6f}".format(
                frameIndex, end-start, fps))

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
                (w, h) = (boxes[i][2], boxes[i][3])

                color = [int(c) for c in colors[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                text = "{}".format(
                    classes[classIDs[i]])
                cv2.putText(frame, text, (x, y-5),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 2)

                print(frameIndex, " ", frameTime,
                      " ", classes[classIDs[i]])

                if classIndex[classIDs[i]] is None:
                    classIndex[classIDs[i]] = [frameIndex]
                else:
                    classIndex[classIDs[i]].append(frameIndex)

        cv2.imshow("Frame", frame)
        videoWrite.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frameIndex += 1

    videoRead.release()
    videoWrite.release()
    cv2.destroyAllWindows()

    detectionInfo = {"classIndex": classIndex, "classes": classes,
                     "baseTimestamp": baseTimestamp, "frameDimensions": (W, H)}

    return detectionInfo


def run():
    init()
    detectionInfo = captureFrames(miscInfo["videoName"])
    DB.update(detectionInfo, miscInfo)
    # runDetection(frame)  will be used after implementing pipelines


if __name__ == "__main__":
    run()

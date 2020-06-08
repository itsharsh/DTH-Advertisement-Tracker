from datetime import datetime
import cv2


def getTimestampFromVideofile(videoName):
    timestamp = videoName.split(".")[0]
    timestamp = datetime.strptime(timestamp, "%Y%m%d-%H%M%S")
    return timestamp


def videoCheck(originalVideo, processedVideo):
    originalRead = cv2.VideoCapture(originalVideo)
    processedRead = cv2.VideoCapture(processedVideo)
    originalVideoFrame = int(originalRead.get(cv2.CAP_PROP_FRAME_COUNT))
    processedVideoFrame = int(processedRead.get(cv2.CAP_PROP_FRAME_COUNT))
    if processedVideoFrame == originalVideoFrame:
        return True
    else:
        return False

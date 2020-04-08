import os
import cv2
from datetime import datetime
from datetime import timedelta
from os import listdir
from os.path import isfile, join


import path_config

adTrackerDir = path_config.adTrackerDir
originalVideoDir = path_config.originalVideoDir
processedVideoDir = path_config.processedVideoDir
recordingVideoDir =path_config.os.path.join(adTrackerDir, "DTH", "Recording")
#VideoFiles = [f for f in listdir(originalVideoDir) if isfile(join(originalVideoDir, f))]
def getTimestampFromVideofile(videoName):
    timestamp = videoName.split(".")[0]
    timestamp = datetime.strptime(timestamp, "%Y%m%d-%H%M%S")
    return timestamp

def addStampToVideo(videoName,subdirs):
    videoRead=cv2.VideoCapture(videoName)
    baseTimestamp = getTimestampFromVideofile(videoName)
    (W, H) = (int(videoRead.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(videoRead.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    fps=int(video.get(cv2.CAP_PROP_FPS))
    base=os.path.splitext(os.path.join(processedVideoDir,subdirs,videoname))[0]
    videoWrite = cv2.VideoWriter(os.path.join(base + ".mp4"),
                                 cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),fps, (W, H))
    frameIndex=video.get(cv2.CAP_PROP_POS_FRAMES)
    print(fps)
    while True:
        (grabbed, frame) = videoRead.read()
        if not grabbed:  # end of video
            break
        frameIndex=video.get(cv2.CAP_PROP_POS_FRAMES)

        frameTime = timedelta(
            seconds=frameIndex/fps)

        cv2.putText(frame, (baseTimestamp+frameTime).strftime("%Y/%m/%d-%H:%M:%S.%f")[:-3], (10, 30),
                    cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 1)
        videoWrite.write(frame)

def convertVideo(videoName,subdirs):
    videoRead=cv2.VideoCapture(videoName)
    baseTimestamp = getTimestampFromVideofile(videoName)
    (W, H) = (int(videoRead.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(videoRead.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    fps=int(video.get(cv2.CAP_PROP_FPS))
    base=os.path.splitext(os.path.join(originalVideoDir,subdirs,videoname))[0]
    videoWrite = cv2.VideoWriter(os.path.join(base + ".mp4"),
                                 cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),fps, (W, H))
    frameIndex=video.get(cv2.CAP_PROP_POS_FRAMES)
    print(fps)
    while True:
        (grabbed, frame) = videoRead.read()
        if not grabbed:  # end of video
            break
        frameIndex=video.get(cv2.CAP_PROP_POS_FRAMES)

        frameTime = timedelta(
            seconds=frameIndex/fps)
        videoWrite.write(frame)

for root,subdir,files in os.walk(recordingVideoDir,topdown=True):
    for subdirs in subdir:
        for videoName in files:
            convertVideo(videoName,subdirs)
            addStampToVideo(videoName,subdirs)

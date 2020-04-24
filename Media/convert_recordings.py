import os
import cv2
import platform
from os import listdir
from time import process_time
from datetime import datetime
from datetime import timedelta
from os.path import isfile, join

import path_config

adTrackerDir = path_config.adTrackerDir
originalVideoDir = path_config.originalVideoDir
processedVideoDir = path_config.processedVideoDir
recordingVideoDir = path_config.recordingVideoDir


def getTimestampFromVideofile(videoName):
    timestamp = videoName.split(".")[0]
    timestamp = datetime.strptime(timestamp, "%Y%m%d-%H%M%S")
    return timestamp


def convert_AddStamp(videoPath, videoName, subFolder):
    print(videoPath)
    print(videoName)
    print(subFolder)

    videoRead = cv2.VideoCapture(videoPath)
    baseTimestamp = getTimestampFromVideofile(videoName)
    (W, H) = (int(videoRead.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(videoRead.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    fps = int(videoRead.get(cv2.CAP_PROP_FPS))

    # if subFolder=="Recordings"

    if subFolder == "a":
        baseProcessed = os.path.splitext(os.path.join(
            processedVideoDir, videoName))[0]
        baseOriginal = os.path.splitext(os.path.join(
            originalVideoDir, videoName))[0]

    else:
        if not os.path.exists(os.path.join(processedVideoDir, subFolder)):
            os.makedirs(os.path.join(processedVideoDir, subFolder))
            print("primtyr")
        if not os.path.exists(os.path.join(originalVideoDir, subFolder)):
            os.makedirs(os.path.join(originalVideoDir, subFolder))

        baseProcessed = os.path.splitext(os.path.join(
            processedVideoDir, subFolder, videoName))[0]
        baseOriginal = os.path.splitext(os.path.join(
            originalVideoDir, subFolder, videoName))[0]

    processedVideoWrite = cv2.VideoWriter(os.path.join(baseProcessed + ".mp4"),
                                          cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (W, H))
    frameIndex = videoRead.get(cv2.CAP_PROP_POS_FRAMES)

    originalVideoWrite = cv2.VideoWriter(os.path.join(baseOriginal + ".mp4"),
                                         cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (W, H))
    print(fps)
    while True:
        (grabbed, frame) = videoRead.read()
        if not grabbed:  # end of video
            break
        Time = process_time()
        frameIndex = videoRead.get(cv2.CAP_PROP_POS_FRAMES)

        frameTime = timedelta(
            seconds=frameIndex/fps)

        originalVideoWrite.write(frame)
        frame_time = process_time()

        cv2.putText(frame, (baseTimestamp+frameTime).strftime("%Y/%m/%d-%H:%M:%S.%f")[:-3], (10, 30),
                    cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 1)
        processedVideoWrite.write(frame)
        frame2_time = process_time()
    clip_time = process_time()
    print("time to process single frame=", frame_time-Time)
    print("time to process clip=", frame2_time-Time)
    print("time to process whole task=", clip_time-clip_startTime)


def run():
    for root, subdir, files in os.walk(recordingVideoDir, topdown=True):
        for video in files:
            videoPath = os.path.join(root, video)
            if platform.system() == "Windows":
                print(platform.system())
                videoName = videoPath.split("\\")[-1]
                subFolder = videoPath.split("\\")[-2]
                clip_startTime = process_time()
                convert_AddStamp(videoPath, videoName, subFolder)

            elif platform.system() == "Linux":
                print(platform.system())
                videoName = videoPath.split("/")[-1]
                subFolder = videoPath.split("/")[-2]
                clip_startTime = process_time()
                convert_AddStamp(videoPath, videoName, subFolder)

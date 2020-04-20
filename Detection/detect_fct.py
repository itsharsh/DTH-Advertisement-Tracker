import os
import csv
import cv2
import logging
import datetime
from time import process_time
from skimage.measure import compare_ssim as ssim

import Detection
import path_config
from DB import update_db as DB

videoPath = path_config.originalVideoDir
clipFileName = path_config.brandFCTFilePath

frames_list = []

miscInfo = {
    "channelName": "tobe",
    "videoName": "20200110-131854.mp4",
    "adType": "FCT",
    "videoFPS": 25,
    "frameToRead": 1  # read every nth frame
}
baseTimestamp = Detection.getTimestampFromVideofile(
    miscInfo["videoName"])
detectionInfo = {"classIndex": frames_list, "classes": path_config.brandName, "baseTimestamp": baseTimestamp,
                 "frameDimensions": (256, 256)}


def detectFCT(videoFile, clipFile, start_time):

    cap1 = cv2.VideoCapture(videoFile)
    cap = cv2.VideoCapture(clipFile)
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    total_frame1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frame, total_frame1)
    list1 = []

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    should_restart = True
    print(fps)
#    cap1.set(cv2.CAP_PROP_POS_FRAMES, 65550)
    while cap1.isOpened or should_restart:
        t1_start = process_time()
        for i in range(int(cap.get(cv2.CAP_PROP_POS_FRAMES)), total_frame):
            # cap.set(cv2.CAP_PROP_POS_FRAMES,i)
            ret, frame = cap.read()
            start = process_time()
            for j in range(int(cap1.get(cv2.CAP_PROP_POS_FRAMES)), total_frame1):
                ts = process_time()
                ret1, frame1 = cap1.read()
                s = ssim(frame, frame1, multichannel=True)
                if s >= .962:
                    print("matched", cap.get(cv2.CAP_PROP_POS_FRAMES), "--",
                          cap1.get(cv2.CAP_PROP_POS_FRAMES), "ssim=", s)
                    list1.append(cap1.get(cv2.CAP_PROP_POS_FRAMES))

                    break
                else:
                    print("not matched", cap.get(cv2.CAP_PROP_POS_FRAMES), "--", cap1.get(cv2.CAP_PROP_POS_FRAMES), "ssim=",
                          s)
                    if len(list1) > 0:
                        list2 = list1
                        frames_list.append(list2)
                        print("appended")
                        list1 = []
                stop = process_time()
                tf = stop - start
                # print("time to process single frame",tf)
            t_stop = process_time()
            time = t_stop - t1_start
            print("time to match frames", time)

        DB.update(detectionInfo, miscInfo)
        t1_stop = process_time()
        print("time taken process approx 500 frames", t1_stop - t1_start)
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == total_frame:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            should_restart = False
        if cap1.get(cv2.CAP_PROP_POS_FRAMES) == total_frame1:
            break
    stop_time = process_time()
    extime = stop_time - start_time
    print("total time taken to execute", extime)
    print(frames_list)


def run():
    for i, folder in enumerate(path_config.detectionChannel):

        miscInfo["channelName"] = folder

        file_list = os.listdir(os.path.join(videoPath, folder))
        for file in file_list:

            if file.split("-")[0] == path_config.detectionDate:
                miscInfo["videoName"] = file
                videoFile = os.path.join(videoPath, folder, file)
                start_time = process_time()
                detectFCT(videoFile, clipFileName, start_time)
# print(miscInfo)
# print(detectionInfo)


run()

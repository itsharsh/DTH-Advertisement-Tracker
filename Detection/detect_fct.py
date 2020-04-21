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

ssimThreshold = .952

miscInfo = {
    "channelName": "",
    "videoName": "",
    "adType": "FCT",
    "videoFPS": 25,
    "frameToRead": 1  # read every nth frame
}

detectionInfo = {"classIndex": None, "classes": path_config.brandName, "baseTimestamp": "",
                 "frameDimensions": (256, 256)}


def detectFCT(videoFile, clipFile, start_time):

    cap1 = cv2.VideoCapture(videoFile)
    cap = cv2.VideoCapture(clipFile)
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frame == 0:
        return print("file not found")
    total_frame1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frame, total_frame1)
    list1 = []

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    should_restart = True
    print(fps)
#    frames_list = []
  #  cap1.set(cv2.CAP_PROP_POS_FRAMES, 65550)
    should_restart = True
    while cap1.isOpened or should_restart:
        frames_list = []
        t1_start = process_time()
        for i in range(int(cap.get(cv2.CAP_PROP_POS_FRAMES)), total_frame):
            # cap.set(cv2.CAP_PROP_POS_FRAMES,i)
            ret, frame = cap.read()
            for j in range(int(cap1.get(cv2.CAP_PROP_POS_FRAMES)), total_frame1):
                ts = process_time()
                ret1, frame1 = cap1.read()

                start = process_time()
                s = ssim(frame, frame1, multichannel=True)
                stop = process_time()
                tf = stop - start
                msg = ""
                if s >= ssimThreshold:
                    msg = "Matched"
                    list1.append(cap1.get(cv2.CAP_PROP_POS_FRAMES))
                else:
                    msg = "Not Matched"
                    if len(list1) > 0:
                        list2 = list1
                        frames_list.append(list2)
                        print("appended")
                        list1 = []
                        print(frames_list)
                print("Time Taken: {:.2f}\tFPS: {:.2f}\t{}\t{} : {}\t SSIM: {:.8f}".format(
                    round(tf, 2), round(1/tf, 2), msg, cap.get(cv2.CAP_PROP_POS_FRAMES), cap1.get(cv2.CAP_PROP_POS_FRAMES), round(s, 8)))

                if (msg == "Matched"):
                    break
        detectionInfo["classIndex"] = frames_list
        print(detectionInfo)
        print(miscInfo)
        print(frames_list)
    #    DB.update(detectionInfo, miscInfo)
    #    frames_list = []
        t1_stop = process_time()
        print("Time Taken to process FCT Clip: ", t1_stop - t1_start)
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == total_frame:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            if len(list1) > 0:
                list2 = list1
                frames_list.append(list2)
                print("appended")
                list1 = []
                print(frames_list)
            #should_restart = False

        if cap1.get(cv2.CAP_PROP_POS_FRAMES) == total_frame1:
            cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
            should_restart = True
            break
    DB.update(detectionInfo, miscInfo)
    stop_time = process_time()
    extime = stop_time - start_time
    print("Total Time Taken: ", extime)
    print(frames_list)


def run():
    for i, folder in enumerate(path_config.detectionChannel):

        miscInfo["channelName"] = folder

        file_list = os.listdir(os.path.join(videoPath, folder))
        for file in file_list:

            if file.split("-")[0] == path_config.detectionDate:
                miscInfo["videoName"] = file
                detectionInfo["baseTimestamp"] = Detection.getTimestampFromVideofile(
                    miscInfo["videoName"])
                videoFile = os.path.join(videoPath, folder, file)
                start_time = process_time()
                detectFCT(videoFile, clipFileName, start_time)
# print(miscInfo)
# print(detectionInfo)


if __name__ == "__main__":
    run()

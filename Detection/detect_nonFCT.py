import os
import cv2
import numpy as np
from time import process_time

import Detection
import path_config
from DB import update_db as DB

max_list1 = []
max_list2 = []
max_list3 = []
aston_frame_list = []
LBand_frame_list = []


miscInfo = {
    "channelName": "",
    "videoName": "",
    "adType": "",
    "videoFPS": 25,
    "frameToRead": 1  # read every nth frame
}
detectionInfo = {"classIndex": None, "classes": None, "baseTimestamp": "",
                 "frameDimensions": (256, 256)}


threshold = .58


def detectNonFCT_astonBand(template, videoFile):
    classes_list = []
    fstart = process_time()
    miscInfo["adType"] = "astonBand"
    print("detection started")

    brand_name = path_config.brandName

    print(template, videoFile)
    list1 = []
    Band = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
    print(Band.shape)
    w, h = Band.shape[::-1]
    video = cv2.VideoCapture(videoFile)
#    video.set(cv2.CAP_PROP_POS_FRAMES, 34000)
    totalFrame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    while video.isOpened:
        frameNo = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        if frameNo == totalFrame:
            break

        ret, frame = video.read()
        start = process_time()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(frame_gray, Band, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0]+w, top_left[1]+h)

        if max_val > threshold:
            msg = "astonBand found"
            cv2.rectangle(frame, top_left, bottom_right, (255, 255, 0), 3)
            list1.append(frameNo)
            classes_list.append(brand_name)

        else:
            msg = "not found"
            if len(list1) > 0:
                msg = "appended to astonBand list"
                list2 = list1
                aston_frame_list.append(list2)
                print("appended")
                list1 = []
        stop = process_time()
        tf = stop-start
        cv2.imshow("detect", frame)
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
       #  FPS: {:.2f}\t   , round(1/tf, 2)
        print("Time Taken: {:.2f}\tFPS: \t{}\t{} : {}\t {:.8f}".format(
            round(tf, 2), msg, miscInfo["adType"], frameNo, round(max_val, 8)))
    print(aston_frame_list)
    detectionInfo["classes"] = classes_list
    detectionInfo["classIndex"] = aston_frame_list
    DB.update(detectionInfo, miscInfo)
    fstop = process_time()
    print("time to process whole video=", fstop-fstart)


def detectNonFCT_LBand(template, template1, videoFile):
    classes_list = []
    fstart = process_time()
    miscInfo["adType"] = "LBand"
    print("detection started")
    print(template, template1,     videoFile)
    list1 = []
    Band1 = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
    print(Band1.shape)
    w1, h1 = Band1.shape[::-1]

    Band2 = cv2.imread(template1, cv2.IMREAD_GRAYSCALE)
    print(Band2.shape)
    w2, h2 = Band2.shape[::-1]

    brand_name = path_config.brandName

    video = cv2.VideoCapture(videoFile)
#    video.set(cv2.CAP_PROP_POS_FRAMES, 34000)

    totalFrame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    while video.isOpened:
        frameNo = video.get(cv2.CAP_PROP_POS_FRAMES)
        if frameNo == totalFrame:
            break

        ret, frame = video.read()
        start = process_time()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res1 = cv2.matchTemplate(frame_gray, Band1, cv2.TM_CCOEFF_NORMED)
        min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
        top_left1 = max_loc1
        bottom_right1 = (top_left1[0]+w1, top_left1[1]+h1)

        res2 = cv2.matchTemplate(frame_gray, Band2, cv2.TM_CCOEFF_NORMED)
        min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
        top_left2 = max_loc2
        bottom_right2 = (top_left2[0]+w2, top_left2[1]+h2)

        if max_val1 > threshold and max_val2 > threshold:
            msg = "LBand found"
            cv2.rectangle(frame, top_left1, bottom_right1, (255, 255, 0), 3)
            cv2.rectangle(frame, top_left2, bottom_right2, (255, 255, 0), 3)
            list1.append(frameNo)
            classes_list.append(brand_name)
        else:
            msg = "not found"
            if len(list1) > 0:
                list2 = list1
                LBand_frame_list.append(list2)
                msg = "appended to LBand list"
                list1 = []
        stop = process_time()
        tf = stop-start
       # cv2.imshow("detect", frame)
        print("Time Taken: {:.2f}\tFPS: {:.2f}\t{}\t{} : {}\t {:.8f}\t {:.8f} ".format(
            round(tf, 2), round(1/tf, 2), msg, miscInfo["adType"], frameNo, round(max_val1, 8), round(max_val2, 8)))
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()

    print(LBand_frame_list)
    detectionInfo["classes"] = classes_list
    detectionInfo["classIndex"] = LBand_frame_list
    DB.update(detectionInfo, miscInfo)
    fstop = process_time()
    print("time to process whole video=", fstop-fstart)


def run():
    tempPath = path_config.brandNonFCTFilePath

    for i in range(len(path_config.detectionChannel)):
        videoPath = os.path.join(path_config.originalVideoDir,
                                 path_config.detectionChannel[i])
        miscInfo["channelName"] = path_config.detectionChannel[i]

        for file in os.listdir(tempPath):
            if file .startswith("Cropped_"+path_config.brandName+"_AstonBand"):
                print("AstonBand template found")
                template = os.path.join(tempPath, file)

                for root, sub, files in os.walk(videoPath):
                    print(videoPath)
                #  miscInfo["channelName"] = videoPath.split()[-1]
                    for videoName in files:
                        if videoName.split("-")[0] == path_config.detectionDate:
                            miscInfo["videoName"] = videoName
                            detectionInfo["baseTimestamp"] = Detection.getTimestampFromVideofile(
                                miscInfo["videoName"])

                            videoFile = os.path.join(videoPath, videoName)
                            print("will detect astonband")
                            detectNonFCT_astonBand(template, videoFile)
            if file.startswith("Cropped_"+path_config.brandName+"_LBand"):
                print("LBand template found")
                if file.endswith("_1.jpeg"):

                    template1 = os.path.join(tempPath, file)

                if file.endswith("_2.jpeg"):
                    template2 = os.path.join(tempPath, file)
                    for root, sub, files in os.walk(videoPath):
                        print(videoPath)
                    #     miscInfo["channelName"] = sub
                        for videoName in files:
                            if videoName.split("-")[0] == path_config.detectionDate:
                                miscInfo["videoName"] = videoName
                                detectionInfo["baseTimestamp"] = Detection.getTimestampFromVideofile(
                                    miscInfo["videoName"])

                                videoFile = os.path.join(videoPath, videoName)
                                print("will detect Lband")
                                detectNonFCT_LBand(
                                    template1, template2, videoFile)


if __name__ == "__main__":
    run()

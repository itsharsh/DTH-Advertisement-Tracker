import os
import cv2
import numpy as np
from time import process_time

import Detection
import path_config
from DB import update_db as DB


tempPath = path_config.brandNonFCTFilePath
tempList = os.listdir(tempPath)
hList = []
wList = []
LBand_hList = []
AstonBand_hList = []
AstonBand_wList = []
LBand_wList = []


resList = []
max_list1 = []
max_list2 = []
max_list3 = []
aston_frame_list = []
L_frame_list = []

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


def detect_NonFCT(videoFile):
    frames_List = []
    list1 = []
    classes_list = []
    video = cv2.VideoCapture(videoFile)
    # video.set(cv2.CAP_PROP_POS_FRAMES, 34000)
    totalFrame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    while video.isOpened:
        # print("readingFrame")
        frameNo = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        if frameNo == totalFrame:
            if len(list1) > 0:

                frames_List.append(list1)
                list1 = []

            detectionInfo["classes"] = classes_list
            detectionInfo["classIndex"] = frames_List
            DB.update(detectionInfo, miscInfo)
            break

        ret, frame = video.read()

        start = process_time()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        max_val_list = []
        max_loc_list = []
        threshold = .55
        for i, temp in enumerate(tempList):
            temp = os.path.join(tempPath, temp)
            Band = cv2.imread(temp, cv2.IMREAD_GRAYSCALE)
#            print("checking all plates")
            res = cv2.matchTemplate(frame_gray, Band, cv2.TM_CCOEFF_NORMED)
            resList.append(res)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            max_loc_list.append(max_loc)
            max_val_list.append(max_val)
        # for i in max_val_list:
        if max(max_val_list) >= threshold:
         #   if (i in max_val_list) >= threshold:
            maxIndex = max_val_list.index(max(max_val_list))
#           print(maxIndex)
            if tempList[maxIndex].startswith("Cropped_"+path_config.brandName+"_LBand"):
                miscInfo["adType"] = "L Band"
                msg = "L Band found"

            elif tempList[maxIndex].startswith("Cropped_"+path_config.brandName+"_AstonBand"):
                miscInfo["adType"] = "Aston Band"
                msg = "Aston Band found"

            top_left = max_loc_list[maxIndex]
            bottom_right = (top_left[0]+wList[maxIndex],
                            top_left[1]+hList[maxIndex])
            classes_list.append(path_config.brandName)
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 255), 2)
            list1.append(frameNo)

        else:
            msg = "nothing matched"
            if len(list1) > 0:
                frames_List.append(list1)
                list1 = []

        stop = process_time()
        tf = stop-start

        print("Time Taken: {:.2f}\tFPS: {:.2f}\t{} \t{} : {}\t {:.8f}\t ".format(
            round(tf, 2), round(1/tf, 2), msg,  miscInfo["adType"], frameNo, round(max(max_val_list), 8)))

        cv2.imshow("detect", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(frames_List)
    video.release()
    cv2.destroyAllWindows()


#   print("*********************")


def run():
    for i, channel in enumerate(path_config.detectionChannel):

        videoPath = os.path.join(path_config.processedVideoDir, channel)
        miscInfo["channelName"] = channel
        for i, temp in enumerate(os.listdir(tempPath)):
            temp = os.path.join(tempPath, temp)
            LBand = cv2.imread(temp, cv2.IMREAD_GRAYSCALE)
            #    print(LBand.shape)
            w, h = LBand.shape[::-1]
            hList.append(h)
            wList.append(w)
        print(hList)
        print(wList)
        # print(wList)
        # print(hList)
        for i, (h, w, temp) in enumerate(zip(hList, wList, tempList)):
            if temp.startswith("Cropped_"+path_config.brandName+"_LBand"):
                # if hList[i] > wList[i]:
                LBand_hList.append(hList[i])
                LBand_wList.append(wList[i])
            elif temp.startswith("Cropped_"+path_config.brandName+"_AstonBand"):
                # elif hList[i] < wList[i]:
                AstonBand_hList.append(hList[i])
                AstonBand_wList.append(wList[i])

        print("GO")

        for root, sub, files in os.walk(videoPath):
            for videoName in files:
                if videoName.split("-")[0] == path_config.detectionDate:
                    miscInfo["videoName"] = videoName
                    detectionInfo["baseTimestamp"] = Detection.getTimestampFromVideofile(
                        miscInfo["videoName"])

                    videoFile = os.path.join(videoPath, videoName)
                    print("will start detection of band")
                    detect_NonFCT(videoFile)


if __name__ == "__main__":
    run()

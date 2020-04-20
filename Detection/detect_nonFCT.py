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
LBand1_frame_list = []
LBand2_frame_list = []

#frame_list = []


videoPath = path_config.originalVideoDir
tempPath = path_config.brandNonFCTFilePath

videoPath = r"C:\Users\Hp\Desktop\testvid"
tempPath = r"C:\Users\Hp\Desktop\Data\Merinolam"
LPath = r"C:\Users\Hp\Desktop\Data\Merinolam\LBand"

threshold = .58


def detectNonFCT(template, videoFile):
    list1 = []
    Band = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
    print(Band.shape)
    w, h = Band.shape[::-1]
    video = cv2.VideoCapture(videoFile)
#video.set(cv2.CAP_PROP_POS_FRAMES, 34000)

    start = process_time()
    while video.isOpened:
        # int(video.get(cv2.CAP_PROP_FRAME_COUNT)):
        if int(video.get(cv2.CAP_PROP_POS_FRAMES)) == int(video.get(cv2.CAP_PROP_FRAME_COUNT)):
            break

        #ret, frame_gray = video.read()
        ret, frame = video.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameNo = video.get(cv2.CAP_PROP_POS_FRAMES)
        # print(frame_gray.shape)
        # print(frameNo)
        # print(Band.shape)

        # Apply template Matching for L BAND test

        res = cv2.matchTemplate(frame_gray, Band, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0]+w, top_left[1]+h)
#        list1 = []

        temptype = template.split("_")[1]
        if max_val > threshold:
            cv2.rectangle(frame, top_left, bottom_right, (255, 255, 0), 3)
            list1.append(frameNo)

        else:
            if len(list1) > 0:
                list2 = list1
                if temptype == "AstonBand":
                    aston_frame_list.append(list2)

                elif temptype == "LBand1":
                    LBand1_frame_list.append(list2)

                elif temptype == "LBand2":
                    LBand2_frame_list.append(list2)
                print("appended")
                list1 = []
        cv2.imshow("detect", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
    stop = process_time()
    print("time to process whole video=", stop-start)

    #  return max_val, top_left, bottom_right
# detectNonFCT(r"C:\Users\Hp\Pictures\LBand2jpg.jpg",
 #            r"C:\Users\Hp\Desktop\20200117-131854ss1.mp4")


# detectNonFCT(r"C:\Users\Hp\Desktop\Merinolam_AstonBand_cropped.jpeg",
#            r"C:\Users\Hp\Desktop\20200117-131854ss1.mp4")


#classList = DB.getStartEnd(frame_list)
# for i, classList in enumerate(aston_frame_list):
#   if classList is not None:
#      classList = DB.getStartEnd(classList)
#     for i in classList:
#        print(i)


    for file in os.listdir(tempPath):
        print(file)
        if file.endswith("cropped.jpeg"):

            template = os.path.join(tempPath, file)
            print(template)
            for files in os.listdir(videoPath):
                videoFile = os.path.join(videoPath, files)
                print(videoFile)
                detectNonFCT(template, videoFile)
            # print(path)
#            print(path.split("_")[1])

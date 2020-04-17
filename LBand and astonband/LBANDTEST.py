import cv2
import numpy as np
from time import process_time

import detect_db
import detect_branding

# LBand1

temp1 = r"C:\Users\Hp\Pictures\LBand1.jpg"
L1Band = cv2.imread(temp1, cv2.IMREAD_GRAYSCALE)
print(L1Band.shape)
w1, h1 = L1Band.shape[::-1]

# LBand2

temp2 = r"C:\Users\Hp\Pictures\LBand2jpg.jpg"
L2Band = cv2.imread(temp2, cv2.IMREAD_GRAYSCALE)
print(L2Band.shape)
w2, h2 = L2Band.shape[::-1]

# astonBand

temp3 = r"C:\Users\Hp\Desktop\aslam ppt\Merinolam_AstonBand_1n.jpeg"
astonBand = cv2.imread(temp3, cv2.IMREAD_GRAYSCALE)
print(astonBand.shape)
astonBand = cv2.resize(astonBand, (720, 100), interpolation=cv2.INTER_NEAREST)
w3, h3 = astonBand.shape[::-1]
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#          'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

max_list1 = []
max_list2 = []
max_list3 = []
aston_frame_list = []
L_frame_list = []
list1 = []


miscInfo = {
    "channelName": "Star Sports 1",
    "videoName": "20200117-213035.mp4",
    "adType": "Non-FCT",
    "videoFPS": 25,
    "frameToRead": 1  # read every nth frame
}
baseTimestamp = detect_branding.getTimestampFromVideofile(
    miscInfo["videoName"])
detectionInfo = {"classIndex": L_frame_list, "classes": "merinolam", "baseTimestamp": baseTimestamp,
                 "frameDimensions": (256, 256)}


# videoFile

#videoFile = r"C:\Users\Hp\Desktop\Data\20200117-125957-3400-3420-Merinolam-Star Sports 1.mp4"
#videoFile = r"C:\Users\Hp\Desktop\20200117-131854.mp4"
videoFile = r"C:\Users\Hp\Desktop\20200117-131854ss1.mp4"
#videoFile = r"C:\Users\Hp\Documents\Bandicut\20200117-131854TestLBand.mp4"
#videoFile = r"C: \Users\Hp\Documents\Bandicut\20200117-131854ss1.mp4"


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
    print(frame_gray.shape)
    print(frameNo)
    print(L1Band.shape)
    print(L2Band.shape)

    # Apply template Matching for L BAND test

    res1 = cv2.matchTemplate(frame_gray, L1Band, cv2.TM_CCOEFF)
    res2 = cv2.matchTemplate(frame_gray, L2Band, cv2.TM_CCOEFF)
    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
    max_list1.append(max_val1)
    max_list1.append(max_val1)
    min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
    max_list2.append(max_val2)
    max_list2.append(max_val2)

    top_left1 = max_loc1
    bottom_right1 = (top_left1[0] + w1, top_left1[1] + h1)
    top_left2 = max_loc2
    bottom_right2 = (top_left2[0]+w2, top_left2[1]+h2)
# Apply templateMAching for aston band

    res3 = cv2.matchTemplate(frame_gray, astonBand, cv2.TM_CCOEFF)
    min_val3, max_val3, min_loc3, max_loc3 = cv2.minMaxLoc(res3)
    max_list3.append(max_val3)
    max_list3.append(max_val3)

    top_left3 = max_loc3
    bottom_right3 = (top_left3[0] + w3, top_left3[1] + h3)
    #print(max_val1,   max_val2)
    threshold1 = 10000000.0
    threshold2 = 110000000.0
    threshold3 = 170000000.0
    #list1 = []
    if max_val1 > threshold1 and max_val2 > threshold2:
        cv2.rectangle(frame, top_left1, bottom_right1, (0, 255, 255), 2)
        cv2.rectangle(frame, top_left2, bottom_right2, (0, 255, 255), 2)
        list1.append(frameNo)
        aston_frame_list.append(frameNo)
        print("LBand Detected")
    elif max_val3 > threshold3:
        cv2.rectangle(frame, top_left3, bottom_right3, (255, 255, 255), 4)
        list1.append(frameNo)
        aston_frame_list.append(frameNo)
        print("aston band detected")
    else:
        if len(list1) > 0:
            list2 = list1
            L_frame_list.append(list2)
            print("appended")
            list1 = []
            #detect_db.updateDB(detectionInfo, miscInfo)


# uncomment next line for viewing Band tracking
    cv2.imshow("detect", frame)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
stop = process_time()
print("time for 1hr video", stop-start)
print(L_frame_list)
# print(aston_frame_list)
#print(max_list1, max_list2,  max_list3)
# print(detect_db.getStartEnd(aston_frame_list))

# print([detect_db.getStartEnd(L_frame_list)])


# comment the below portion of code and uncomment line 126 to test for generating csv file             #detect_db.updateDB(detectionInfo, miscInfo)
for i, classList in enumerate(L_frame_list):
    if classList is not None:
        classList = detect_db.getStartEnd(classList)
        for i in classList:
            print(i)

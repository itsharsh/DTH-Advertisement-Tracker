import sys
import cv2
import imutils
import pandas as pd
import numpy as np
dataFilePath = "/home/vivek/Test/CSV/adtrack.csv"
workingDirectory = "/home/vivek/Test/Ad Clips"
dataset=pd.read_csv(dataFilePath)
channelNameList=np.array(dataset['Channel Name'])
adClipFileName=np.array(dataset['Clip File Name'])
adBrandNameArray = np.array(dataset['Brand Name'])
adStartTime=np.array(dataset['Ad Frame Start'])
adEndTime=np.array(dataset['Ad Frame End'])
prop=cv2.CAP_PROP_FRAME_COUNT
fileIndex = 0
while (fileIndex<adClipFileName.size):
    print(fileIndex)
    path="/home/vivek/Test/Ad Clips/"+str(adBrandNameArray[fileIndex])+"/"+channelNameList[fileIndex]+"/"+adClipFileName[fileIndex]+".mp4"
    print(path)
    video=cv2.VideoCapture(path)
    print(adStartTime[fileIndex]*0.04,adEndTime[fileIndex]*0.04)
    total=int(video.get(prop))
    #print(adClipFileName[fileIndex])
    print("frames: ",total)
    fileIndex+=1



# import cv2
# video=cv2.VideoCapture('/home/vivek/Test/test.mp4')
# total=int(video.get(7))
# print(total)
# print(total*0.04)
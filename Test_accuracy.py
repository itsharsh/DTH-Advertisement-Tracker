import cv2
import pandas as pd
import numpy as np
dataFilePath = "/home/vivek/AdTracker/CSV/adtrack.csv"
workingDirectory = "/home/vivek/AdTraker/DTH/Ad Clips/"
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
    path=workingDirectory+str(adBrandNameArray[fileIndex])+"/"+channelNameList[fileIndex]+"/"+adClipFileName[fileIndex]+".mp4"
    print(path)
    video=cv2.VideoCapture(path)
    print(adStartTime[fileIndex]*0.040,adEndTime[fileIndex]*0.040)
    total=int(video.get(prop))
    print("frames: ",total)
    print("Duration",total*0.040)
    fileIndex+=1



# import cv2
# video=cv2.VideoCapture("/home/vivek/AdTracker/DTH/Ad Clips/Kamla Pasand/Star Sports 1/ds-20200117-de-ts-213035-te-xs-0.28-xe-ys-1.28-ye-ads-Kamla Pasand-ade-chs-Star Sports 1-che.mp4")
# prop=cv2.CAP_PROP_FRAME_COUNT
# total=int(video.get(prop))
# print(total)
# print(total*0.04)
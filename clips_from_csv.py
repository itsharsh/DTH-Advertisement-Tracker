import os
import numpy as np
import pandas as pd
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

channelNameList = ["Star Sports 1", "Star Sports 1 Hindi"]
workingDirectory = "/home/vivek/Test"
videoDataPath = workingDirectory+"/Original"
outputDataPath = workingDirectory+"/Ad Clips"
dataFilePath = "/home/vivek/Test/CSV/20200117-213035-17000-1f.csv"
makeDirectoryCommand = "mkdir -p \""+outputDataPath+"\""
print(makeDirectoryCommand)
os.system(makeDirectoryCommand)

for channelName in channelNameList:
    print("Cutting clips in "+channelName)

    dataset = pd.read_csv(dataFilePath)
    print("--------------------After Reading data:--------------------")
    print("Dataset:")
    print(dataset)
    dataset = dataset[dataset['Channel Name'] == channelName]
    dataset = dataset.reset_index()
    dataset = dataset.drop("index", axis=1)
    print("--------------------After Filterting data:-----------------")

    dataset = dataset[dataset['Channel Name'] == channelName]
    dataset = dataset.reset_index()
    dataset = dataset.drop("index", axis=1)

    fileNameArray = np.array(dataset['Source File'])
    channelNameArray = np.array(dataset['Channel Name'])
    adBrandNameArray = np.array(dataset['Brand Name'])
    print(fileNameArray)
    fileTimeStampArray = pd.to_datetime(
        dataset['Source File'], errors='coerce', format="%Y%m%d-%H%M%S")
    print(fileTimeStampArray)

    adStartTimeArray = pd.to_timedelta(dataset['Ad Start'])
    adEndTimeArray = pd.to_timedelta(dataset['Ad End'])
    adDurationArray = adEndTimeArray-adStartTimeArray
    adClipFileName=np.array(dataset['Clip File Name'])
    adStartTime=np.array(dataset['Ad Frame Start'])
    adEndTime=np.array(dataset['Ad Frame End'])
    print(dataset)

    fileIndex = 0
    while(fileIndex < fileNameArray.size):
        print("Cutting file: "+str(fileIndex+1) +
              " "+adBrandNameArray[fileIndex])
        makeDirectoryPath = outputDataPath+"/" + \
            adBrandNameArray[fileIndex]+"/" + channelNameArray[fileIndex]
        print(makeDirectoryPath)
        os.system("mkdir -p \""+makeDirectoryPath+"\"")
        sourceFile=videoDataPath+"/"+str(fileNameArray[fileIndex])+".mp4"
        outPutFile=makeDirectoryPath+"/"+str(adClipFileName[fileIndex])+".mp4"
        print(sourceFile)
        print(outPutFile)
        print(adStartTime[fileIndex]-1,adEndTime[fileIndex]+1)
        ffmpeg_extract_subclip(sourceFile,adStartTime[fileIndex]*0.04,adEndTime[fileIndex]*0.04,outPutFile)
        #terminalCommand = "ffmpeg -n -i \""+videoDataPath+"/" + \
        #    str(fileNameArray[fileIndex])+".mp4\""+" -ss " + \
        #    str(adStartTime[fileIndex]) + " -t " + \
        #    str(adDurationArray[fileIndex].total_seconds()+1) + " \"" + \
        #        makeDirectoryPath+"/"+adClipFileName[fileIndex]+".mp4\""


        #print(terminalCommand)
        #print(os.popen(terminalCommand).read())
        fileIndex += 1

    print(channelName+" Completed")

print("Task Completed Successfully")

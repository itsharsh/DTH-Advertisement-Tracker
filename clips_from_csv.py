import os
import numpy as np
import pandas as pd

channelNameList = ["Star Sports 1", "Star Sports 1 Hindi"]
workingDirectory = "/mnt/6C8CA6790B328288/Projects/AI/AdTracker/DTH"
videoDataPath = workingDirectory+"\Original"
outputDataPath = workingDirectory+"\Ad Clips"
dataFilePath = "CSV/adtrack.csv"

makeDirectoryCommand = "mkdir \""+outputDataPath+"\""
print(makeDirectoryCommand)
# os.system(makeDirectoryCommand)

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

    fileNameArray = np.array(dataset['Time Stamp'])
    channelNameArray = np.array(dataset['Channel Name'])
    adBrandNameArray = np.array(dataset['Ad Brand Name'])
    print(fileNameArray)
    fileTimeStampArray = pd.to_datetime(
        dataset['Time Stamp'], errors='coerce', format="%Y%m%d-%H%M%S")
    print(fileTimeStampArray)

    adStartTimeArray = pd.to_timedelta(dataset['Ad Start'])
    adEndTimeArray = pd.to_timedelta(dataset['Ad End'])
    adDurationArray = adEndTimeArray-adStartTimeArray
    print(dataset)

    fileIndex = 0
    while(fileIndex < fileNameArray.size):
        print("Cutting file: "+str(fileIndex+1) +
              " "+adBrandNameArray[fileIndex])
        makeDirectoryPath = outputDataPath+"\\" + \
            adBrandNameArray[fileIndex]+"\\" + channelNameArray[fileIndex]
        print(makeDirectoryPath)
        # os.system("mkdir \""+makeDirectoryPath+"\"")
        terminalCommand = "ffmpeg -n -i \""+videoDataPath+"\\"+channelName+"\\" + \
            fileNameArray[fileIndex]+".mp4\""+" -ss " + \
            str(adStartTimeArray[fileIndex].total_seconds()) + " -t " + \
            str(adDurationArray[fileIndex].total_seconds()) + " \"" + \
            makeDirectoryPath+"\\"+fileNameArray[fileIndex] + \
            "-" + str(int(adStartTimeArray[fileIndex].total_seconds())) + \
            "-" + str(int(adEndTimeArray[fileIndex].total_seconds())) + \
            "-" + adBrandNameArray[fileIndex]+"-"+channelName+".mp4\""

        print(terminalCommand)
        # print(os.popen(terminalCommand).read())
        fileIndex += 1

    print(channelName+" Completed")

print("Task Completed Successfully")

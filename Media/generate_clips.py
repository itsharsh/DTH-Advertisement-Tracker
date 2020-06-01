import os
import numpy as np
import pandas as pd

import path_config

adTrackerDir = path_config.adTrackerDir
dbFilePath = path_config.dbFilePath
clipsDir = path_config.clipsDir
processedVideoDir = path_config.processedVideoDir
NonFCTVideoDir = path_config.NonFCTVideoDir
FCTVideoDir = path_config.FCTVideoDir

channelNameList = ["Star Sports 1", "Star Sports 1 Hindi"]
NonFCT=["L Band","Aston Band"]
makeDirectoryCommand = "mkdir -p \"{}\"".format(clipsDir)
print(makeDirectoryCommand)
os.system(makeDirectoryCommand)

def run():
    for channelName in channelNameList:
        print("Cutting clips in "+channelName)

        dataset = pd.read_csv(dbFilePath)
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
        adTypeArray=np.array(dataset['Type of Ad'])
        print(fileNameArray)
        fileTimeStampArray = pd.to_datetime(
            dataset['Source File'], errors='coerce', format="%Y%m%d-%H%M%S")
        print(fileTimeStampArray)

        adClipFileName = np.array(dataset['Clip File Name'])
        adStartTime = np.array(dataset['Ad Frame Start'])
        adEndTime = np.array(dataset['Ad Frame End'])
        adDurationArray = adEndTime-adStartTime
        print(dataset)

        fileIndex = 0
        while(fileIndex < fileNameArray.size):
            print("Cutting file: "+str(fileIndex+1) +
                " "+adBrandNameArray[fileIndex])
            makeDirectoryPath = os.path.join(
                clipsDir, adBrandNameArray[fileIndex], channelNameArray[fileIndex])
            print(makeDirectoryPath)
            os.system("mkdir -p \""+makeDirectoryPath+"\"")
            if adTypeArray[fileIndex]=="Branding":
                sourceFile = os.path.join(processedVideoDir, "Branding", channelName, str(
                    fileNameArray[fileIndex]))+".mp4"
            elif adTypeArray[fileIndex]=="FCT":
                sourceFile = os.path.join(FCTVideoDir, "FCT", channelName, str(
                    fileNameArray[fileIndex]))+".mp4"
            for bandType in NonFCT:
                if adTypeArray[fileIndex]==bandType :
                    sourceFile = os.path.join(NonFCTVideoDir, "NonFCT", channelName, str(
                        fileNameArray[fileIndex]))+".mp4"
            outPutFile = os.path.join(makeDirectoryPath, str(
                adClipFileName[fileIndex]))+".mp4"

            print(sourceFile)
            print(outPutFile)
            print(adStartTime[fileIndex]*0.040, adEndTime[fileIndex]*0.040)
            terminalCommand = "ffmpeg -n -i \"{}\" -ss {} -t {} \"{}/{}.mp4\"".format(
                sourceFile,
                str(adStartTime[fileIndex] * 0.040),
                str(adDurationArray[fileIndex]*0.040),
                makeDirectoryPath, adClipFileName[fileIndex])
            print(terminalCommand)
            print(os.popen(terminalCommand).read())
            fileIndex += 1

        print(channelName+" Completed")

    print("Ad Clips Created Successfully")

import csv
import sys
import pandas as pd
from datetime import timedelta

adTrackerDirectory = "D:/Office/Backup/Projects Data/AI/AdTracker/"
csvFilePath = "CSV/"
csvFileName = "adtrack.csv"


def getStartEnd(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))


def updateDBIndex():
    try:
        df = pd.read_csv(csvFilePath+csvFileName)
        return df["DB Index"].max()+1  # add 1 for counter

    except pd.errors.EmptyDataError:
        print("Empty CSV File")
        return 1


def updateCSV(row):
    with open(csvFilePath+csvFileName, mode='a+', newline='') as csvFile:
        fileWriter = csv.writer(csvFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(row)


def updateDB(detectionInfo, miscInfo):
    try:
        for i, classList in enumerate(detectionInfo["classIndex"]):
            if classList is not None:
                classList = getStartEnd(classList)
                for startEnd in classList:
                    index = updateDBIndex()
                    sourceFile = miscInfo["videoName"].split(".")[0]
                    brandName = detectionInfo["classes"][i]

                    date = detectionInfo["baseTimestamp"].date()

                    adFrameStart = startEnd[0]
                    adFrameEnd = startEnd[1]
                    adClipStart = timedelta(
                        seconds=adFrameStart/miscInfo["frameToRead"])
                    adClipEnd = timedelta(
                        seconds=adFrameEnd/miscInfo["frameToRead"])
                    duration = (adClipEnd-adClipStart).total_seconds()

                    adStart = ((detectionInfo["baseTimestamp"]+adClipStart).time()
                               ).strftime("%H:%M:%S.%f")[:-3]
                    adEnd = ((detectionInfo["baseTimestamp"]+adClipEnd).time()
                             ).strftime("%H:%M:%S.%f")[:-3]

                    clipFileName = "ds-{}-de-ts-{}-te-xs-{}-xe-ys-{}-ye-ads-{}-ade-chs-{}-che".format(
                        sourceFile.split("-")[0], sourceFile.split("-")[1],
                        int((adFrameStart/miscInfo["videoFPS"]) * 1000),
                        int((adFrameEnd/miscInfo["videoFPS"])*1000),
                        detectionInfo["classes"][i], miscInfo["channelName"])

                    header = ["DB Index", "Channel Name", "Type of Ad", "Brand Name",
                              "Date", "Ad Start", "Ad End", "Duration", "Clip File Name",
                              "Source File", "Ad Frame Start", "Ad Frame End"]
                    row = [index, miscInfo["channelName"], miscInfo["adType"], brandName,
                           date, adStart, adEnd, duration, clipFileName,
                           sourceFile, adFrameStart, adFrameEnd]

                    if index == 1:
                        updateCSV(header)
                    updateCSV(row)
                    print("DB Updated")
    except FileNotFoundError:
        csvCreate = open(csvFilePath+csvFileName, mode='w', newline='')
        updateDB(detectionInfo, miscInfo)
    except:
        print("Exception while updating DB: ", sys.exc_info())

import os
import csv
import sys
import platform
import pandas as pd
from datetime import timedelta

if platform.system() == "Windows":
    adTrackerDirectory = "D:/Office/Backup/Projects Data/AI/AdTracker/"
elif platform.system() == "Linux":
    adTrackerDirectory = "/mnt/6C8CA6790B328288/Projects/AI/AdTracker/"

csvFilePath = "CSV"
csvFileName = "adtrack.csv"


def getStartEnd(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))


def updateDBIndex():
    try:
        df = pd.read_csv(os.path.join(csvFilePath, csvFileName))
        return df["DB Index"].max()+1  # add 1 for counter

    except pd.errors.EmptyDataError:
        print("Empty CSV File")
        return 1


def updateCSV(row):
    with open(os.path.join(csvFilePath, csvFileName), mode='a+', newline='') as csvFile:
        fileWriter = csv.writer(csvFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow(row)


def updateDB(detectionInfo, miscInfo):
    try:
        for i, classList in enumerate(detectionInfo["classIndex"]):
            if classList is not None:

                classList = getStartEnd(classList)
                for startEnd in classList:
                    sourceFile = miscInfo["videoName"].split(".")[0]

                    index = updateDBIndex()
                    brandName = detectionInfo["classes"][i]

                    date = detectionInfo["baseTimestamp"].date()

                    adFrameStart = startEnd[0]
                    adFrameEnd = startEnd[1]

                    adClipStart = timedelta(
                        seconds=adFrameStart/miscInfo["videoFPS"])
                    adClipEnd = timedelta(
                        seconds=adFrameEnd/miscInfo["videoFPS"])
                    adStart = ((detectionInfo["baseTimestamp"]+adClipStart).time()
                               ).strftime("%H:%M:%S.%f")[:-3]
                    adEnd = ((detectionInfo["baseTimestamp"]+adClipEnd).time()
                             ).strftime("%H:%M:%S.%f")[:-3]

                    duration = (adClipEnd-adClipStart).total_seconds()

                    clipFileName = "ds-{}-de-ts-{}-te-xs-{}-xe-ys-{}-ye-ads-{}-ade-chs-{}-che".format(
                        sourceFile.split("-")[0], sourceFile.split("-")[1],
                        adClipStart.total_seconds(), adClipEnd.total_seconds(),
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
        csvCreate = open(os.path.join(
            csvFilePath, csvFileName), mode='w', newline='')
        updateDB(detectionInfo, miscInfo)
    except:
        print("Exception while updating DB: ", sys.exc_info())

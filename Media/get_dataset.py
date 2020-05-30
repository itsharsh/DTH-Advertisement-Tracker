import os
import cv2
import glob
import time
import shutil
import ntpath
import zipfile
from sklearn.model_selection import train_test_split

videoDir = "/mnt/6C8CA6790B328288/Projects/AI/AdTracker/DTH/"
workdir = "/home/harsh/darknetdata/"
dataDir = workdir+"Dataset/"  # For storing .txt and .jpg in respective folders
annotationZIPDir = workdir+"Annotations/"
trainFilename = "train.txt"
testFilename = "test.txt"
outputExtention = ".jpg"
imageQuality = 50


def createDirectory(path):
    try:
        os.mkdir(path)
        print("Created: ", path)
    except FileExistsError:
        print("Already exists: ", path)


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = []
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


def extractZIPFile(annotationZIPFile, annotationZIPFileName):
    print("Extracting: "+annotationZIPFile)
    try:
        with zipfile.ZipFile(annotationZIPFile, "r") as z:
            z.extractall(annotationZIPDir+annotationZIPFileName)
        print("ZIP Extraction Completed: "+annotationZIPFile)
    except FileNotFoundError:
        print("ZIP file not found")


def preProcess(k):
    return int(k[6:12])


def getFrameList(annotationZIPFileName):
    frameList = [preProcess(k) for k in os.listdir(
        annotationZIPDir+annotationZIPFileName) if k.endswith(".txt")]
    frameList.sort()
    return frameList


def extractFrames(videoPath, videoFileName, selectedFrames):
    print("Capturing Frames from: "+videoFileName+".mp4")
    try:
        i = 0
        j = 0
        prevj = 0
        createDirectory(dataDir+videoFileName)
        print("Total Sets to be created: " +
              str(int(selectedFrames[len(selectedFrames)-1] / 1000)))
        createDirectory(dataDir+videoFileName+"/"+str(j))
        while i < len(selectedFrames):
            j = int(selectedFrames[i] / 1000)
            if prevj != j:
                createDirectory(dataDir+videoFileName+"/"+str(j))
                prevj = j
            # ffmpeg
            # os.system("ffmpeg -hide_banner -loglevel panic -i \"{videoFileName}\" -vf select='eq(n\,{frameno})' -vsync 0 -start_number {frameno} \"{outputDir}/frame_%06d.jpg\" ".format(
            #     videoFileName=videoPath, outputDir=dataDir+videoFileName, frameno=selectedFrames[i]))

            # opencv
            cap = cv2.VideoCapture(videoPath)
            cap.set(1, selectedFrames[i])
            ret, frame = cap.read()
            cv2.imwrite(dataDir+videoFileName+"/"+str(j)+"/frame_%s.jpg" %
                        str(selectedFrames[i]).zfill(6), frame, [cv2.IMWRITE_JPEG_QUALITY, imageQuality])
            cap.release()

            annotationFile = "/frame_" + str(selectedFrames[i]).zfill(6)+".txt"

            shutil.move(annotationZIPDir+videoFileName+annotationFile,
                        dataDir+videoFileName+"/"+str(j) + annotationFile)

            i += 1
        print("Capturing Frames Completed: "+videoFileName)
    except FileNotFoundError:
        print("File not found in extractZIPFile")


def generateTestTrain(annotationZIPFileName):
    try:
        allFiles = glob.glob(dataDir+annotationZIPFileName+"/*/*.txt")
        fileList = [sub.replace('.txt', outputExtention) for sub in allFiles]
        Train, Test = train_test_split(fileList, test_size=0.2, random_state=0)
        for path in Train:
            file_train.write(path + "\n")
        for path in Test:
            file_test.write(path + "\n")
    except ValueError:
        print("Empty dataset")
    print("Test Train Generated Successfully")
    print("Total Dataset: "+str(len(allFiles)))


start = time.time()
createDirectory(annotationZIPDir)
createDirectory(dataDir)
createDirectory(videoDir)
file_train = open(annotationZIPDir+trainFilename, 'w')
file_test = open(annotationZIPDir+testFilename, 'w')
file_train = open(annotationZIPDir+'train.txt', 'a+')
file_test = open(annotationZIPDir+'test.txt', 'a+')

for annotationZIPFile in getListOfFiles(annotationZIPDir):
    annotationZIPFileName = os.path.splitext(
        ntpath.basename(annotationZIPFile))[0]
    if(annotationZIPFile.endswith(".zip")):
        extractZIPFile(annotationZIPFile, annotationZIPFileName)

        for video in getListOfFiles(videoDir):
            videoFileName = os.path.splitext(ntpath.basename(video))[0]
            if(annotationZIPFileName == videoFileName):
                selectedFrames = getFrameList(annotationZIPFileName)
                extractFrames(video, videoFileName, selectedFrames)

        generateTestTrain(annotationZIPFileName)

print("Completed")

print("Time taken: {} seconds".format(time.time()-start))

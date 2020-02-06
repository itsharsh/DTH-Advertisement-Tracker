import os
import cv2
import glob
import shutil
import ntpath
import zipfile
from sklearn.model_selection import train_test_split

print(cv2.__version__)
workdir = os.getcwd() + "/"  # Ubuntu
# workdir = "D:/Projects Data/AI/"  # Windows
dataDir = workdir+"Dataset/"  # For storing .txt and .jpg in respective folders
# For storing .zip folder
annotationsDir = workdir+"Annotations/"
# For storing .mp4 folder
# videoDir = workdir+"Videos/"
videoDir = "/mnt/6C8CA6790B328288/Projects/AI/AdTracker/DTH/"


def createDirectory(path):
    try:
        os.mkdir(path)
        print("Created: ", path)
    except FileExistsError:
        print("Already exists: ", path)


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


def extractZIPFile(zipFileName):
    print("Extracting: "+zipFileName+".zip")
    try:
        with zipfile.ZipFile(annotationsDir+annotationFileName+".zip", "r") as z:
            z.extractall(dataDir+annotationFileName)
        print("ZIP Extraction Completed: "+annotationFileName)
    except FileNotFoundError:
        print("ZIP file not found")


def preProcess(k):
    return int(k[6:12])


def getFrameList(annotationFileName):
    frameList = [preProcess(k) for k in os.listdir(
        dataDir+annotationFileName) if k.endswith(".txt")]
    frameList.sort()
    return frameList


def extractFrames(videoPath, videoFileName, selectedFrames):
    print("Capturing Frames from: "+videoFileName+".mp4")
    try:
        i = 0
        while i < len(selectedFrames):
            # ffmpeg
            # os.system("ffmpeg -hide_banner -loglevel panic -i \"{videoFileName}\" -vf select='eq(n\,{frameno})' -vsync 0 -start_number {frameno} \"{outputDir}/frame_%06d.jpg\" ".format(
            #     videoFileName=videoPath, outputDir=dataDir+videoFileName, frameno=selectedFrames[i]))

            # opencv
            cap = cv2.VideoCapture(videoPath)
            cap.set(1, selectedFrames[i])
            ret, frame = cap.read()
            cv2.imwrite(dataDir+videoFileName+"/frame_%s.jpg" %
                        str(selectedFrames[i]).zfill(6), frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            cap.release()
            i += 1
        print("Capturing Frames Completed: "+videoFileName)
    except FileNotFoundError:
        print("MP4 file not found")


def generateTestTrain(annotationFileName):
    allFiles = glob.glob(dataDir+annotationFileName+"/*.txt")
    fileList = [sub.replace('txt', 'jpg') for sub in allFiles]
    Train, Test = train_test_split(fileList, test_size=0.2, random_state=0)
    file_train = open(dataDir+'atrain.txt', 'a+')
    file_test = open(dataDir+'atest.txt', 'a+')
    for path in Train:
        file_train.write(path + "\n")
    for path in Test:
        file_test.write(path + "\n")


createDirectory(annotationsDir)
createDirectory(dataDir)
createDirectory(videoDir)
file_train = open(dataDir+'atrain.txt', 'w')
file_test = open(dataDir+'atest.txt', 'w')

for annotation in getListOfFiles(annotationsDir):
    annotationFileName = os.path.splitext(ntpath.basename(annotation))[0]
    annotationFileNameExt = os.path.splitext(ntpath.basename(annotation))[1]
    if(annotationFileNameExt == ".zip"):
        # extractZIPFile(annotationsDir+annotationFileName)

        for video in getListOfFiles(videoDir):
            videoFileName = os.path.splitext(ntpath.basename(video))[0]
            if(annotationFileName == videoFileName):
                selectedFrames = getFrameList(annotationFileName)
                # extractFrames(video, videoFileName, selectedFrames)

        generateTestTrain(annotationFileName)

print("Completed")

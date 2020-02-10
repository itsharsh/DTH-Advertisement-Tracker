import os
import cv2
import glob
import shutil
import ntpath
import zipfile
from sklearn.model_selection import train_test_split

print(cv2.__version__)
imagesDir = "/home/harsh/Optimized Images/"
# imagesDir = "/mnt/6C8CA6790B328288/Projects/AI/Situational Awareness System/Weapons Dataset/Optimized Images/"
workdir = "/home/harsh/Dataset for Training/"

annotationZIPDir = workdir
dataDir = workdir+"Dataset/"
trainFilename = "train.txt"
testFilename = "test.txt"
outputExtention = ".JPG"


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


def extractZIPFile(annotationZIPFile, annotationZIPFileName):
    print("Extracting: "+annotationZIPFile)
    try:
        with zipfile.ZipFile(annotationZIPFile, "r") as z:
            z.extractall(dataDir+annotationZIPFileName)
        print("ZIP Extraction Completed: "+annotationZIPFile)
    except FileNotFoundError:
        print("ZIP file not found")


def generateTestTrain():
    allFiles = glob.glob(imagesDir+"/*/*.txt")
    fileList = [sub.replace('.txt', outputExtention) for sub in allFiles]
    Train, Test = train_test_split(fileList, test_size=0.2, random_state=0)
    for path in Train:
        file_train.write(path + "\n")
    for path in Test:
        file_test.write(path + "\n")


createDirectory(annotationZIPDir)
createDirectory(dataDir)
createDirectory(imagesDir)
file_train = open(workdir+trainFilename, 'w')
file_test = open(workdir+testFilename, 'w')
file_train = open(workdir+'train.txt', 'a+')
file_test = open(workdir+'test.txt', 'a+')

imageList = []
imageListPath = []
for image in getListOfFiles(imagesDir):
    imageListPath.append(image)
    imageList.append(os.path.splitext(ntpath.basename(image))[0])

for annotationZIPFile in getListOfFiles(annotationZIPDir):
    annotationZIPFileName = os.path.splitext(
        ntpath.basename(annotationZIPFile))[0]
    if(annotationZIPFile.endswith(".zip")):
        extractZIPFile(annotationZIPFile, annotationZIPFileName)
        i = 0

        for txtFile in getListOfFiles(dataDir+annotationZIPFileName+"/"):
            if txtFile.endswith(".txt"):
                file = os.path.splitext(ntpath.basename(txtFile))[0]
                try:
                    dest = imageListPath[imageList.index(file)]
                    shutil.move(txtFile, dest[:-4]+".txt")
                    i += 1
                except ValueError:
                    pass

        print("Total Annotations: "+str(i))

generateTestTrain()

print("Completed")

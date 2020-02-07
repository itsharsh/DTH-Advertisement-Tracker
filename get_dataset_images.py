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
# For storing .JPG folder
imagesDir = "/mnt/6C8CA6790B328288/Projects/AI/Situational Awareness System/Weapons Dataset/Optimized Images/"
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


def extractZIPFile(zipFileName):
    print("Extracting: "+zipFileName+".zip")
    try:
        with zipfile.ZipFile(annotationsDir+annotationFileName+".zip", "r") as z:
            z.extractall(dataDir+annotationFileName)
        print("ZIP Extraction Completed: "+annotationFileName)
    except FileNotFoundError:
        print("ZIP file not found")


def generateTestTrain(annotationFileName):
    allFiles = glob.glob(dataDir+annotationFileName+"/*.txt")
    fileList = [sub.replace('.txt', outputExtention) for sub in allFiles]
    Train, Test = train_test_split(fileList, test_size=0.2, random_state=0)
    file_train = open(dataDir+'train.txt', 'a+')
    file_test = open(dataDir+'test.txt', 'a+')
    for path in Train:
        file_train.write(path + "\n")
    for path in Test:
        file_test.write(path + "\n")


createDirectory(annotationsDir)
createDirectory(dataDir)
createDirectory(imagesDir)
file_train = open(dataDir+trainFilename, 'w')
file_test = open(dataDir+testFilename, 'w')

for annotation in getListOfFiles(annotationsDir):
    annotationFileName = os.path.splitext(ntpath.basename(annotation))[0]
    annotationFileNameExt = os.path.splitext(ntpath.basename(annotation))[1]
    if(annotationFileNameExt == ".zip"):
        extractZIPFile(annotationsDir+annotationFileName)
        i = 0
        for image in getListOfFiles(imagesDir):
            if image.endswith(outputExtention):
                imageFileName = os.path.splitext(ntpath.basename(image))[0]
                shutil.copyfile(
                    image, dataDir+"/"+annotationFileName+"/"+imageFileName+outputExtention)
                i += 1
        print("Total Images: "+str(i))

        generateTestTrain(annotationFileName)

print("Completed")

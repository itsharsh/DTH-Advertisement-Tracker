import os
import cv2
import glob
import ntpath
import zipfile
#from sklearn.model_selection import train_test_split

print(cv2.__version__)
workdir = os.getcwd() + "/" # Ubuntu
# workdir = "D:/Projects Data/AI/"  # Windows
dataDir = workdir+"Dataset/"  # For storing .txt and .jpg in respective folders
# For storing .zip folder
annotationsDir = workdir+"Annotations/"
# For storing .mp4 folder
videoDir = workdir+"Videos/"
# videoDir = "/mnt/6C8CA6790B328288/Projects/AI/AdTracker/DTH/"


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


def preProcess(k):
    '''
    input format frame_000019.txt
    output 19
    '''
    return int(k[6:12])




def extractZIPFile(zipFileName):
    print("Extracting: "+zipFileName)
    try:
        with zipfile.ZipFile(annotationsDir+annotationFileName+".zip", "r") as z:
            z.extractall(dataDir+annotationFileName)
        print("ZIP Extraction Completed: "+annotationFileName)
    except FileNotFoundError:
        print("ZIP file not found")


def extractFrames(videoPath, videoFileName):
    print("Capturing Frames from: "+videoFileName)
    try:
        vidcap = cv2.VideoCapture(videoPath)
        success, image = vidcap.read()
        count = 0
        while success:
            cv2.imwrite(dataDir+videoFileName+"/frame_%s.jpg" %
                        str(count).zfill(6), image)
            success, image = vidcap.read()
            # print('Read frame: ', count, success)
            count += 1
        print("Capturing Frames Completed: "+videoFileName)
    except FileNotFoundError:
        print("MP4 file not found")


def generateTestTrain():
    print("Generating Test Train:")
    listOfFiles = glob.glob(dataDir+"/*/"+"/*.txt")
    listOfFiles = [sub.replace('txt', 'jpg') for sub in listOfFiles]
    Train, Test = train_test_split(listOfFiles, test_size=0.2, random_state=0)
    file_train = open(dataDir+'train.txt', 'w')
    file_test = open(dataDir+'test.txt', 'w')
    for path in Train:
        file_train.write(path + "\n")
    for path in Test:
        file_test.write(path + "\n")

    print("Completed")

video_file_list = []
for annotation in getListOfFiles(annotationsDir):
    annotationFileName = os.path.splitext(ntpath.basename(annotation))[0]
    annotationFileNameExt = os.path.splitext(ntpath.basename(annotation))[1]
    if(annotationFileNameExt == ".zip"):
        extractZIPFile(annotationsDir+annotationFileName)

        for video in getListOfFiles(videoDir):
            videoFileName = os.path.splitext(ntpath.basename(video))[0]
            if(annotationFileName == videoFileName):
                video_file_list.append(videoFileName)
                extractFrames(video, videoFileName)
                text_files  = [preProcess(k) for k in os.listdir(dataDir + videoFileName) if k.endswith(".txt")]
                frame_files = [preProcess(k) for k in os.listdir(dataDir + videoFileName) if k.endswith(".jpg")]
                frame_difference = set(frame_files).difference(set(text_files))
                for k in frame_difference:
                    k+=1
                    jpg_name = "frame_{:06d}.jpg".format(k)
                    if os.path.exists(dataDir + videoFileName + '/' +jpg_name):
                        os.remove(dataDir + videoFileName + '/' +jpg_name)

#generateTestTrain()






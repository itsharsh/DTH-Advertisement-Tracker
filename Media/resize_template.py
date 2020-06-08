import cv2
#import glob
import os
import path_config

tempPath = path_config.brandNonFCTFilePath
tempList = os.listdir(tempPath)

inputFolder=tempPath
folderLen = len (inputFolder)
os.mkdir(os.path.join(path_config.brandNonFCTFilePath,"resized"))


def tempResize(temp,W,H): 
    temp = cv2.imread(temp, cv2.IMREAD_UNCHANGED)
    
    print('Original Dimensions : ',temp.shape)

    shapeX=max(temp.shape[0],temp.shape[1])
    if shapeX==temp.shape[0]:
        scaleFactor= W*100/shapeX
    elif shapeX==temp.shape[1]:
        scaleFactor=H*100/shapeX
#    scaleFactor= max(scaleFactor1,scaleFactor2)
    #print(scaleFactor1,     scaleFactor2    , scaleFactor)
    width = int(temp.shape[1] * scaleFactor / 100)
    height = int(temp.shape[0] * scaleFactor / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(temp, dim, interpolation = cv2.INTER_AREA)
    
    print('Resized Dimensions : ',resized.shape)
    return resized



#for img in glob.glob (inputFolder + "/*.jpg"):
for i, temp in enumerate(tempList):
    img= os.path.join(tempPath,temp)
#    image=cv2.imread(img)
    imgResized = tempResize(img,576,720)
    cv2.imwrite (os.path.join(path_config.brandNonFCTFilePath,"resized") + img[folderLen:], imgResized)
    cv2.imshow ('image', imgResized)
    cv2.waitKey(30)
cv2.destroyAllWindows= cv2.imread (img)


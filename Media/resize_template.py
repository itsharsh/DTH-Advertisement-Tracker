import cv2
import os
import fnmatch
import path_config

tempPath = path_config.brandNonFCTFilePath
frameDimension = path_config.frameDimension


def tempResize(temp, W, H):
    temp = cv2.imread(temp, cv2.IMREAD_UNCHANGED)

    print('Original Dimensions : ', temp.shape)

    shapeX = max(temp.shape[0], temp.shape[1])
    if shapeX == temp.shape[0]:
        scaleFactor = W*100/shapeX
    elif shapeX == temp.shape[1]:
        scaleFactor = H*100/shapeX
    #    scaleFactor= max(scaleFactor1,scaleFactor2)
        #print(scaleFactor1,     scaleFactor2    , scaleFactor)
    width = int(temp.shape[1] * scaleFactor / 100)
    height = int(temp.shape[0] * scaleFactor / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(temp, dim, interpolation=cv2.INTER_AREA)

    print('Resized Dimensions : ', resized.shape)
    return resized


def run():
    tempList = fnmatch.filter(os.listdir(tempPath), '*.jpeg')
    print(tempList)

    inputFolder = tempPath
    folderLen = len(inputFolder)
    if not os.path.exists(os.path.join(path_config.brandNonFCTFilePath, "Resized")):
        os.mkdir(os.path.join(path_config.brandNonFCTFilePath, "Resized"))
    # for img in glob.glob (inputFolder + "/*.jpg"):
    for i, temp in enumerate(tempList):
        img = os.path.join(tempPath, temp)
    #    image=cv2.imread(img)
        imgResized = tempResize(img, frameDimension[0], frameDimension[1])
        print(frameDimension[0], frameDimension[1])
        cv2.imwrite(os.path.join(path_config.brandNonFCTFilePath,
                                 "Resized") + img[folderLen:], imgResized)
        cv2.imshow('image', imgResized)
        cv2.waitKey(30)
    cv2.destroyAllWindows = cv2.imread(img)


if __name__ == "__main__":
    run()

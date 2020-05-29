import os
import platform

if platform.system() == "Windows":
    if(os.getlogin() == "Harsh"):
        adTrackerDir = os.path.join("D:\\", "Test", "AdTracker")
    elif(os.getlogin() == "Ajeet"):
        adTrackerDir = os.path.join("D:\\", "Test", "AdTracker")
elif platform.system() == "Linux":
    if(os.getlogin() == "harsh"):
        adTrackerDir = os.path.join(
            "/media", "harsh", "HDD", "Projects Data", "AdTracker")
    elif(os.getlogin() == "vivek"):
        adTrackerDir = os.path.join(
            "/home", "vivek", "Projects Data", "AdTracker")

dbFilePath = os.path.join(adTrackerDir, "DB", "adtrack.csv")

modelDir = os.path.join(adTrackerDir, "Model")
originalVideoDir = os.path.join(adTrackerDir, "Videos", "Original")
recordingVideoDir = os.path.join(adTrackerDir, "Videos", "Recordings")
processedVideoDir = os.path.join(adTrackerDir, "Videos", "Processed", "NonFCT")
clipsDir = os.path.join(adTrackerDir, "Videos", "Ad Clips")

brandingModelName = "49_Ads"
brandingModelConfigPath = os.path.join(
    modelDir, brandingModelName, brandingModelName + "_test.cfg")
brandingModelClassesPath = os.path.join(
    modelDir, brandingModelName, brandingModelName + ".names")
brandingModelWeightsPath = os.path.join(
    modelDir, brandingModelName, brandingModelName + "_last.weights")

detectionDate = "20200117"
detectionChannel = ["Star Sports 1"]
detectionAd = []
brandName = "Merinolam"

brandDir = os.path.join(adTrackerDir, "Brand Data", brandName)

brandFCTFilePath = os.path.join(brandDir, brandName+"_FCT.mp4")
brandNonFCTFilePath = os.path.join(brandDir, "Cropped_"+brandName)

import os
import platform

if platform.system() == "Windows":
    adTrackerDir = os.path.join("D:\\", "Test", "AdTracker")
    # adTrackerDir = os.path.join(
    # "D:\\", "Office", "Backup", "Projects Data", "AI", "AdTracker")
    gitRepoDir = os.path.join(
        "D:\\", "Office", "Google Drive", "Projects", "AI", "AdTracker", "Adtracker")
elif platform.system() == "Linux":
    adTrackerDir = "/home/vivek/AdTracker/"
    gitRepoDir = os.path.join("/home/vivek/", "AdTracker")

dbDir = os.path.join(gitRepoDir, "DB")
dbFilePath = os.path.join(dbDir, "adtrack.csv")

modelDir = os.path.join(adTrackerDir, "Model")
originalVideoDir = os.path.join(adTrackerDir, "DTH", "Original")
processedVideoDir = os.path.join(adTrackerDir, "DTH", "Processed")
recordingVideoDir = os.path.join(adTrackerDir, "DTH", "Recordings")
clipsDir = os.path.join(adTrackerDir, "DTH", "Ad Clips")

brandingModelName = "49_Ads"
brandingModelConfigPath = os.path.join(
    modelDir, brandingModelName, brandingModelName + "_test.cfg")
brandingModelClassesPath = os.path.join(
    modelDir, brandingModelName, brandingModelName + ".names")
brandingModelWeightsPath = os.path.join(
    modelDir, brandingModelName, brandingModelName + "_last.weights")

detectionDate = "20191211"
detectionChannel = ["Star Sports 1", "Star Sports 1 Hindi"]
detectionAd = []
brandName = "Merinolam"

brandDir = os.path.join(adTrackerDir, "Brand Data", brandName)

brandFCTFilePath = os.path.join(brandDir, brandName+"_FCT.mp4")
brandNonFCTFilePath = os.path.join(brandDir, "Cropped_"+brandName, "*.jpeg")

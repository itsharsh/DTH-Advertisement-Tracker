'''
@desc : Program to scan the directory of annotations and
generate only those whose frames are present

main_folder structure
    -separate.py
    -image
        -frame001.jpg
        -frame002.jpg
    -annotation
        -frame001.jpg
    -image_with_annotation (the desired images will be stored here. 
    mkdir this folder before running the script)


'''


import os
import zipfile
import ffmpeg
import cv2
import time

def extract_all_zip(zip_files):
    print(zip_files)
    for zip_ in zip_files:
        destination = loc +'/' +zip_[:-4]
        with zipfile.ZipFile(zip_,"r") as zip_ref:
            zip_ref.extractall(destination)

def preProcess(k):
    '''
    input format frame_000019.txt
    output 19
    '''
    return int(k[6:12])

    


loc = os.getcwd()
zip_files = [i for i in os.listdir(loc) if i[-3:] == "zip"]
mp4_files = [i for i in os.listdir(loc) if i[-3:] == "mp4"]

# extract zip
# extract image

extract_all_zip(zip_files)


    


for i in zip(zip_files,mp4_files):
    if i[0][:-4] == i[1][:-4]:
        select_frame = [preProcess(k) for k in os.listdir(loc +'/'+ i[0][:-4]) if k.endswith(".txt")]
        
        select_frame.sort()
    
        os.system("ffmpeg -i {a}.mp4 -r 25/1 {a}/frame_%06d.jpg".format(a = i[1][:-4]))
        location = i[1][:-4] + "/"
        select_frame_with_txt = [preProcess(k) for k in os.listdir(loc +'/'+ i[0][:-4]) if k.endswith(".jpg")]

        need_deletion = set(select_frame_with_txt).difference(select_frame)

        

        for k in need_deletion:
            k = k + 1
            jpg_name = "frame_{:06d}.jpg".format(k)
            if os.path.exists(location+jpg_name):
                os.remove(location+jpg_name)


            
        
        
        


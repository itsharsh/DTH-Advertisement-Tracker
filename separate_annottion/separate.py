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
loc = os.getcwd()

for i in os.listdir(loc + "/annotation/"):
    for j in os.listdir(loc + "/image/"):
        if i[:-3]==j[:-3]: #i.e the name match
            source_img = loc + "/image/" + j
            source_anno = loc + "/annotation/" + i
            dest = loc + "/image_with_annotation/" + j
            dest_anno = loc + "/image_with_annotation/" + i
            os.rename(source_img,dest)
            os.rename(source_anno,dest_anno)


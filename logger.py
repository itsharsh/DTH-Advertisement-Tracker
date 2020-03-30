# -*- coding: utf-8 -*-
"""Logger.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nb_ghT2D5B9dCU9cFUfcoZLCEvjkMryw
"""

import cv2
from skimage.measure import compare_ssim as ssim

source_file="ad02.mp4"
clip="ad13.mp4"

cap=cv2.VideoCapture(source_file)
cap1=cv2.VideoCapture(clip)
total_frame=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
total_frame1=int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
print(total_frame, total_frame1)
m=0
frames_list=[]
import logging



channelName="Star Sports 1"
typeOfAd="AdTypeUnknown"
BrandName="Paytm"
clipName="adfile"
adFrame=m
# create logger
lgr = logging.getLogger("logger")
lgr.setLevel(logging.DEBUG) # log all escalated at and above DEBUG
# add a file handler
fh = logging.FileHandler('path_of_your_log2.csv')
fh.setLevel(logging.DEBUG) # ensure all messages are logged to file

# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')

fh.setFormatter(frmt)

# add the Handler to the logger
lgr.addHandler(fh)



fps=int(cap.get(cv2.CAP_PROP_FPS))

print(fps)
while cap.isOpened:
    
      for i in range (total_frame):
          cap.set(cv2.CAP_PROP_POS_FRAMES,i)
          ret,frame=cap.read()
          for j in range (total_frame1):
              cap1.set(cv2.CAP_PROP_POS_FRAMES,j)
              ret1,frame1=cap1.read()
              diff=cv2.subtract(frame,frame1)
              b, g, r =cv2.split(diff)
              s = ssim(frame,frame1, multichannel = True)
              if (cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0) or s>=.97:
                  print("matched",cap.get(cv2.CAP_PROP_POS_FRAMES), "--",cap1.get(cv2.CAP_PROP_POS_FRAMES),"ssim=",s)
                  
                  frames_list.append(cap.get(cv2.CAP_PROP_POS_FRAMES))
                  m+=1
                  
                  break
              else:
                
                print("not matched", cap.get(cv2.CAP_PROP_POS_FRAMES),"--",cap1.get(cv2.CAP_PROP_POS_FRAMES),"ssim=",s)
         
      adStart=frames_list[1]
      adEnd=frames_list[-1]
      Duration=adEnd-adStart
      adFrame=len(frames_list)

      print("total frames matched=",m)
      lgr.info("{},{},{},{},{},{},{},{}".format(channelName,typeOfAd,BrandName,adStart,adEnd,Duration,clipName,adFrame))
      
      break     
print(frames_list)
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import cv2
import numpy as np
import imutils
from libRoad import webCam
import serial
import signal, sys
from yoloOpencv import opencvYOLO

video_out = "output/"#webcam_size  = (1920, 1080)
webcam_size  = (960, 540)
rotatePIC = 0
frameRate = 10.0
comPort = "COM5"   #PC的TTL2USB port
baudRate = 4800

yolo = opencvYOLO(modeltype="yolov3-tiny", \
    objnames="cfg.road_edge.tiny\\obj.names", \
    weights="cfg.road_edge.tiny\\yolov3-tiny_500000.weights",\
    cfg="cfg.road_edge.tiny\\yolov3-tiny.cfg")

def getGPS():
    out = ''
    ynDATA = False
    dataE1, dataE2, dataE3, dataE4 = 0, 0, 0, 0
    dataN1, dataN2, dataN3, dataN4 = 0, 0, 0, 0
	
    try:
        while(serial.inWaiting()):
            out = str(serial.readline().decode('utf-8'))

    except:
        pass	
	
    if out != '':
        gpsdata = out.split(",")
        print(out)


        if(gpsdata[0] == "$GPGGA"):
            dataE = gpsdata[4]
            dataN = gpsdata[2]
            if(len(dataE)>=10):
                dataE1, dataE2, dataE3, dataE4 = dataE[:3], dataE[3:5], dataE[6:8], dataE[8:10]
                ynDATA = True
            if(len(dataN)>=9):
                dataN1, dataN2, dataN3, dataN4 = dataN[:2], dataN[2:4], dataN[5:7], dataN[7:9]
				
    gpsE = "E {}-{}-{}-{}".format(dataE1, dataE2, dataE3, dataE4)
    gpsN = "N {}-{}-{}-{}".format(dataN1, dataN2, dataN3, dataN4)
    print(gpsE, gpsN)
	
    return ynDATA, gpsE, gpsN

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    fo.write(str(frameID) + "|" + dataE + "/" + dataN + "\n" )
    sys.exit(0)
	
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
	
    cam = webCam(id=0, size=webcam_size)
    serial = serial.Serial(comPort, baudRate)
    out = ''
    dataE = dataN = "0"
    frameID = 0
    lastE, lastN = "", ""
    if(cam.working() is True):
        
        if(video_out!=""):
            filename = video_out+str(time.time())
            (width, height) = cam.camRealSize()
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(video_out+str(time.time())+".avi",fourcc, frameRate, (int(width),int(height)))
            fo = open(filename + ".gps", "w")
        print("Video size is ", (width, height))
        while True:
            hasFrame, frame = cam.takepic(rotate=rotatePIC, vflip=False, hflip=False, resize=None, savePath=None)
            ynDATA, tmpE, tmpN = getGPS()
            if(ynDATA == True):
                dataE, dataN = tmpE, tmpN
			
            if not hasFrame:
                print("Done processing !!!")
                cv2.waitKey(3000)
                break

            yolo.getObject(frame, labelWant="", drawBox=True, bold=2, textsize=1.2, bcolor=(0,255,0), tcolor=(0,0,255))
            print ("Object counts:", yolo.objCounts)
			
            cv2.putText(frame, dataE+" / "+dataN, (280,60), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0,0,0), 2)
            cv2.imshow("Frame", imutils.resize(frame, width=850) )
            if(video_out!=""):
                out.write(frame)
                if(lastE != dataE or lastN!=dataN):
                    fo.write(str(frameID) + "|" + dataE + "/" + dataN + "\n" )

                lastE, lastN = dataE, dataN
                frameID += 1
				 
            inkey = cv2.waitKey(1)

    else:
        print("Web camera is not working.")	
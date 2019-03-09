#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, datetime
import cv2
import numpy as np
import imutils
from libRoad import webCam
import serial
import signal, sys

video_out = "output\\"
webcam_size  = (1920, 1080)
rotatePIC = 0
frameRate = 10.0
comPort = "COM5"   #PC的TTL2USB port
baudRate = 4800

def getGPS():
    out = ''
    ynDATA = False
    dataE1, dataE2 = 0.0, 0.0
    dataN1, dataN2 = 0.0, 0.0
    gpsE, gpsN = 0.0, 0.0
    str_gpsE, str_gpsN = "", ""
	
    try:
        while(serial.inWaiting()):
            out = str(serial.readline().decode('utf-8'))

    except:
        pass	
	
    if out != '':
        gpsdata = out.split(",")
        print(out)


        if(gpsdata[0] == "$GPRMC"):
            dataE = gpsdata[5]
            dataN = gpsdata[3]
            if(len(dataE)>=10):
                dataE1, dataE2 = float(dataE[:3]), float(dataE[3:])
                gpsE = round(dataE1 + dataE2/60, 4)
                ynDATA = True
            if(len(dataN)>=9):
                dataN1, dataN2 = float(dataN[:2]), float(dataN[2:])
                gpsN = round(dataN1 + dataN2/60, 4)
				
    str_gpsE = str(gpsE)
    str_gpsN = str(gpsN)
    print(gpsE, gpsN)
	
    return ynDATA, str_gpsE, str_gpsN

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    now = datetime.datetime.now()
    time_data = "{}{}{}{}{}{}".format(now.year,str(now.month).zfill(2),str(now.day).zfill(2),\
        str(now.hour).zfill(2),str(now.minute).zfill(2),str(now.second).zfill(2))
    fo.write(str(frameID) + "|" + time_data + "|" + dataN + "," + dataE + "\n" )
    sys.exit(0)
	
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
	
    cam = webCam(id=0, videofile="", size=webcam_size)
    serial = serial.Serial(comPort, baudRate)
    out = ''
    dataE = dataN = "0"
    frameID = 0
    lastE, lastN = "", ""
    if(cam.working() is True):        
        if(video_out!=""):
            now = datetime.datetime.now()
            filename = "{}年{}月{}日{}點{}分{}秒".format(now.year,now.month,now.day,str(now.hour).zfill(2),str(now.minute).zfill(2),str(now.second).zfill(2))
            (width, height) = cam.camRealSize()
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(video_out+filename+".avi",fourcc, frameRate, (int(width),int(height)))
            fo = open(video_out+filename + ".gps", "w")
        print("Video size is ", (width, height))
        while True:
            hasFrame, frame = cam.takepic(rotate=rotatePIC, vflip=False, hflip=False, resize=None, savePath=None)
            now = datetime.datetime.now()
            time_data = "{}{}{}{}{}{}".format(now.year,str(now.month).zfill(2),str(now.day).zfill(2),\
                str(now.hour).zfill(2),str(now.minute).zfill(2),str(now.second).zfill(2))
			
            ynDATA, tmpE, tmpN = getGPS()
            if(ynDATA == True):
                dataE, dataN = tmpE, tmpN
			
            if not hasFrame:
                print("Done processing !!!")
                cv2.waitKey(3000)
                break

            #cv2.putText(frame, dataN+" , "+dataE, (280,60), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0,0,0), 2)
            cv2.imshow("Frame", imutils.resize(frame, width=850) )
            if(video_out!=""):
                out.write(frame)
                if(lastE != dataE or lastN!=dataN):
                    fo.write(str(frameID) + "|" + time_data + "|" + dataN + "," + dataE + "\n" )

                lastE, lastN = dataE, dataN
                frameID += 1
				 
            inkey = cv2.waitKey(1)

    else:
        print("Web camera is not working.")	
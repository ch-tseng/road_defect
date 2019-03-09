#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, datetime
import cv2
import numpy as np
import imutils
from libRoad import webCam
import serial
import signal, sys
from yoloOpencv import opencvYOLO
import gmaps
from gmplot import gmplot
gmaps.configure(api_key='AIzaSyCbQibjl5FKhsQCFz8lj1ad3qru1bUCdrU')

cam_id = 0
video_file_play = "1550799908.6317935.avi"
gps_file_play = "1550799908.6317935.gps"

video_type = 1  # 0--> webcam  1--> video file

write_video_out = True  #output video or not
video_out = "output"
defect_out = "defect"
#webcam_size  = (1920, 1080)
webcam_size  = (960, 540)
rotatePIC = 0
frameRate = 10.0
comPort = "COM5"   #PC的TTL2USB port
baudRate = 4800

yolo = opencvYOLO(modeltype="yolov3-tiny", \
    objnames="cfg.road_edge.tiny\\obj.names", \
    weights="cfg.road_edge.tiny\\yolov3-tiny_500000.weights",\
    cfg="cfg.road_edge.tiny\\yolov3-tiny.cfg")

if(video_type == 1):
    gps_frames = []
    gps_file = open(gps_file_play, 'r', encoding='UTF-8')
    
    for line in gps_file.readlines():
        gps_frame_id, gps_data = line.split("|")
        if(int(gps_frame_id)>=0):
            gps_frames.append( (int(gps_frame_id), gps_data) )

    print("GPS:", gps_frames)

def getGPS(frameid = 0):
    if(video_type==0):
        out = ''
        ynDATA = False
        dataE1, dataE2 = 0.0, 0.0
        dataN1, dataN2 = 0.0, 0.0
    
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
                    gpsE = dataE1 + dataE2/60
                    ynDATA = True
                if(len(dataN)>=9):
                    dataN1, dataN2 = float(dataN[:2]), float(dataN[2:])
                    gpsN = dataN1 + dataN2/60
                
        str_gpsE = str(gpsE)
        str_gpsN = str(gpsN)

    else:
        ynDATA = False
        for i in range(0, len(gps_frames)-1):
            if( frameID>=int(gps_frames[i][0]) and frameID<int(gps_frames[i+1][0])):
                print(frameID, gps_frames[i][0], gps_frames[i][1])

                gpsN, gpsE = gps_frames[i][1].split(",")
                ynDATA = True

        #now_loc = (float(gpsE), float(gpsN))
        gmap = gmplot.GoogleMapPlotter(float(gpsN), float(gpsE), 18)
        print("GPS:", float(gpsN), float(gpsE))
        if(float(gpsN)>0) and float(gpsE)>0:
            # Marker
            print(gpsN, gpsE)
            #gmap.plot(float(gpsN), float(gpsE), 'cornflowerblue', edge_width=10)
            gmap.marker(float(gpsN), float(gpsE), color='#000000', c=None, title="Defect")
            #gmap.scatter(float(gpsE), float(gpsN),'#FF6666', edge_width=10)
            # Draw
            #gmap.coloricon = "pointer.png"
            gmap.apikey = 'AIzaSyCbQibjl5FKhsQCFz8lj1ad3qru1bUCdrU'
            gmap.draw("my_map.html")

            #print(gpsN, gpsE)
                
    return ynDATA, float(gpsE), float(gpsN)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    fo.write(str(frameID) + "|" + dataN + "," + dataE + "\n" )
    sys.exit(0)
	
def log_defect(img, img_defect, gps_data):
    now = datetime.datetime.now()
    log_time = "{}_{}_{}_{}_{}_{}".format(now.year,now.month,now.day,now.hour,now.minute,now.second)
    print("d_{}_{}_{}.jpg".format(gps_data[0],gps_data[1],log_time))
    print("o_{}_{}_{}.jpg".format(gps_data[0],gps_data[1],log_time))	
    filename_defect = "d_{}_{}_{}.jpg".format(gps_data[0],gps_data[1],log_time)
    filename_org = "o_{}_{}_{}.jpg".format(gps_data[0],gps_data[1],log_time)
    #print(filename_defect)	
    cv2.imwrite(defect_out + "\\" + filename_defect, img_defect )
    cv2.imwrite(defect_out + "\\" + filename_org, img)	
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    if(video_type==0):    
        cam = webCam(id=cam_id, videofile="", size=webcam_size)
    else:
        cam = webCam(videofile=video_file_play, size=webcam_size)
        
    serial = serial.Serial(comPort, baudRate)
    out = ''
    dataE = dataN = "0"
    frameID = 0
    lastE, lastN = "", ""
    if(cam.working() is True):
        
        if(video_out!=""):
            filename = video_out+str(time.time())
            (width, height) = cam.camRealSize()
            if(write_video_out is True):            
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                out = cv2.VideoWriter(video_out+str(time.time())+".avi",fourcc, frameRate, (int(width),int(height)))
                fo = open(filename + ".gps", "w")
                print("Video size is ", (width, height))

        while True:
            hasFrame, frame = cam.takepic(rotate=rotatePIC, vflip=False, hflip=False, resize=None, savePath=None)
            frame = imutils.resize(frame, width=800)
            frame_org = frame.copy()			

            ynDATA, tmpE, tmpN = getGPS()
            if(ynDATA == True):
                dataE, dataN = tmpE, tmpN
            
            if not hasFrame:
                print("Done processing !!!")
                cv2.waitKey(3000)
                break

            yolo.getObject(frame, labelWant="", drawBox=True, bold=2, textsize=1.2, bcolor=(0,255,0), tcolor=(0,0,255))
            print ("Object counts:", yolo.objCounts)
            if(yolo.objCounts>0 and ynDATA is True):
                defect_lists = yolo.listLabels()
                log_defect(frame_org, frame, (dataN, dataE))
            
            cv2.putText(frame, str(dataE)+" / "+str(dataN), (280,30), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,0), 2)
            cv2.imshow("Frame", frame )
            if(write_video_out is True):
                out.write(frame)
                if(lastE != dataE or lastN!=dataN):
                    fo.write(str(frameID) + "|" + str(dataN) + "," + str(dataE) + "\n" )

            lastE, lastN = dataE, dataN
            frameID += 1
                 
            inkey = cv2.waitKey(1)

    else:
        print("Web camera is not working.")    
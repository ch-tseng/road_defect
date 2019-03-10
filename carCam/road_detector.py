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
from gmplot import gmplot
from PIL import ImageFont, ImageDraw, Image
from urllib.request import urlopen

#--------------------------------------------------
gm_apikey = 'AIzaSyBPxuoRArkJBsCVa_e0DCEzo9UuPP-r_Bk'

video_type = 1  # 0--> cam_id  1--> video_file_play
cam_id = 0
cam_size  = (1920, 1080)  #(1920, 1080)

rotatePIC = 0
frameRate = 5.0
video_file_play = "1550799908.6317935.avi"
gps_file_play = "1550799908.6317935.gps"
video_upload_size = cam_size
video_yolo_size = (960, 540)

write_video_out = True  #output video or not
video_out_type = 2  #0--> original video, 1--> obj detected video, 2--> desktop video
video_out = "output\\"  #write video to this folder
defect_detect_out = "defect\\detect\\"  #write defect image to this folder for upload
defect_original_out = "defect\\original\\"  #write defect image to this folder for upload
 

comPort = "COM5"   #PC的TTL2USB port
baudRate = 4800

desktop_size = (800, 480) 
desktop_frame_size = (610,344)  # video size on the desktop bg.
#--------------------------------------------------

yolo = opencvYOLO(modeltype="yolov3-tiny", \
    objnames="cfg.road_edge.tiny\\obj.names", \
    weights="cfg.road_edge.tiny\\yolov3-tiny_500000.weights",\
    cfg="cfg.road_edge.tiny\\yolov3-tiny.cfg")

#gmaps = googlemaps.Client(key=gm_apikey)
#--------------------------------------------------
def conn_test():
    try:
        response = urlopen('http://www.google.com', timeout=1)
        return True
    except urllib2.URLError as err:
        return False	
	
	
def getGPS(frameid = 0):
    if(video_type==0):
        out = ''
        ynDATA = False
        dataE1, dataE2 = 0.0, 0.0
        dataN1, dataN2 = 0.0, 0.0
        gpsE , gpsN = 0.0, 0.0   
		
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
                
        #str_gpsE = str(gpsE)
        #str_gpsN = str(gpsN)

    else:
        ynDATA = False
        for i in range(0, len(gps_frames)-1):
            if( frameID>=int(gps_frames[i][0]) and frameID<int(gps_frames[i+1][0])):
                print(frameID, gps_frames[i][0], gps_frames[i][1], gps_frames[i][2])

                gpsN, gpsE = gps_frames[i][2].split(",")
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
            gmap.apikey = gm_apikey
            gmap.draw("my_map.html")

            #print(gpsN, gpsE)
                
    return ynDATA, float(gpsE), float(gpsN)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    now = datetime.datetime.now()
    time_data = "{}{}{}{}{}{}".format(now.year,str(now.month).zfill(2),str(now.day).zfill(2),\
        str(now.hour).zfill(2),str(now.minute).zfill(2),str(now.second).zfill(2))
    fo.write(str(frameID) + "|" + time_data + "|" + str(dataN) + "," + str(dataE) + "\n" )
    fo.close()
    if(write_video_out is True):
        out.release()
    sys.exit(0)
	
def log_defect(img, img_defect, gps_data):
    now = datetime.datetime.now()
    log_time = "{}_{}_{}_{}_{}_{}".format(now.year,now.month,now.day,now.hour,now.minute,now.second)
    print("d_{}_{}_{}.jpg".format(gps_data[0],gps_data[1],log_time))
    print("o_{}_{}_{}.jpg".format(gps_data[0],gps_data[1],log_time))	
    filename_defect = "d_{}_{}_{}.jpg".format(gps_data[0],gps_data[1],log_time)
    filename_org = "o_{}_{}_{}.jpg".format(gps_data[0],gps_data[1],log_time)
    #print(filename_defect)	
    cv2.imwrite(defect_detect_out + filename_defect, img_defect )
    cv2.imwrite(defect_original_out + filename_org, img)	

def desktop_bg(img, gps, txt_display):
    img = imutils.resize(img, width=desktop_frame_size[0], height=desktop_frame_size[1])
    now = datetime.datetime.now()
    display_time1 = "{}年{}月{}日".format(now.year,now.month,now.day)
    display_time2 = "{}:{}:{}".format(str(now.hour).zfill(2),str(now.minute).zfill(2),str(now.second).zfill(2))
	
    bg = bg_fresh.copy()
    img_shape = img.shape
    dataN, dataE = gps[0], gps[1]
    bg[75:75+img_shape[0], 23:23+img_shape[1]] = img

    #Date
    bg = printText(display_time1, bg, color=(0,0,0,0), size=0.40, pos=(660,85), type="Chinese")
    #Time
    #cv2.putText(bg, display_time2, (680,125), cv2.FONT_HERSHEY_COMPLEX, 0.65, (0,0,0), 1)
    bg = printText(display_time2, bg, color=(0,0,0,0), size=0.45, pos=(680,105), type="Chinese")

    #GPS
    #cv2.putText(bg, "N: "+str(dataN), (660,175), cv2.FONT_HERSHEY_COMPLEX, 0.66, (0,255,0), 2)
    #cv2.putText(bg, "E:"+str(dataE), (660,195), cv2.FONT_HERSHEY_COMPLEX, 0.66, (0,255,0), 2)
    bg = printText("N: "+str(dataN), bg, color=(0,255,0,0), size=0.70, pos=(660,175), type="English")
    bg = printText("E:"+str(dataE), bg, color=(0,255,0,0), size=0.70, pos=(660,200), type="English")
    
    if(len(txt_display)>0):
        bg = printText(txt_display, bg, color=(0,0,255,0), size=0.8, pos=(80,430), type="Chinese")
	
    return bg

def printText(txt, bg, color=(0,255,0,0), size=0.7, pos=(0,0), type="Chinese"):
    (b,g,r,a) = color

    if(type=="English"):
        ## Use cv2.FONT_HERSHEY_XXX to write English.
        cv2.putText(bg,  txt, pos, cv2.FONT_HERSHEY_SIMPLEX, size,  (b,g,r), 2, cv2.LINE_AA)

    else:
        ## Use simsum.ttf to write Chinese.
        fontpath = "fonts/wt009.ttf"
        font = ImageFont.truetype(fontpath, int(size*10*4))
        img_pil = Image.fromarray(bg)
        draw = ImageDraw.Draw(img_pil)
        draw.text(pos,  txt, font = font, fill = (b, g, r, a))
        bg = np.array(img_pil)

    return bg
	
#load GPS data from file if play the video file
if(video_type == 1):
    gps_frames = []
    gps_file = open(gps_file_play, 'r', encoding='UTF-8')
    
    for line in gps_file.readlines():
        gps_frame_id, time_data, gps_data = line.split("|")
        if(int(gps_frame_id)>=0):
            gps_frames.append( (int(gps_frame_id), float(time_data), gps_data) )

if __name__ == "__main__":

    if(conn_test() is False):
        print("No internet connection.")
        exit()

    signal.signal(signal.SIGINT, signal_handler)
    serial = serial.Serial(comPort, baudRate)
    out = ''
    dataE = dataN = "0"
    frameID = 0
    lastE, lastN = "", ""
    bg_fresh = cv2.imread("bg.jpg")
	
    if(video_type==0):    
        cam = webCam(id=cam_id, videofile="", size=cam_size)
    else:
        cam = webCam(videofile=video_file_play, size=cam_size)
        
    if(cam.working() is True):
        
        if(video_out!=""):
            (width, height) = cam.camRealSize()
            if(write_video_out is True):
                now = datetime.datetime.now()
                video_output_file = "{}年{}月{}日{}點{}分{}秒".format(now.year,now.month,now.day,str(now.hour).zfill(2),str(now.minute).zfill(2),str(now.second).zfill(2))            
                #video_output_file = "{}{}{}{}{}{}".format(now.year,now.month,now.day,str(now.hour).zfill(2),str(now.minute).zfill(2),str(now.second).zfill(2)) 
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                if(video_out_type==0):
                    out = cv2.VideoWriter(video_out+video_output_file+".avi",fourcc, frameRate, (cam_size[0],cam_size[1]))
                elif(video_out_type==1):
                    out = cv2.VideoWriter(video_out+video_output_file+".avi",fourcc, frameRate, (video_yolo_size[0],video_yolo_size[1]))
                elif(video_out_type==2):
                    out = cv2.VideoWriter(video_out+video_output_file+".avi",fourcc, frameRate, (desktop_size[0],desktop_size[1]))
					
                fo = open(video_out+video_output_file+".gps", "w")
                print("Video size is ", (width, height))

        while True:
            hasFrame, frame = cam.takepic(rotate=rotatePIC, vflip=False, hflip=False, resize=None, savePath=None)
            frame_org = frame.copy()
            frame = imutils.resize(frame, width=video_yolo_size[0], height=video_yolo_size[1])

            ynDATA, tmpE, tmpN = getGPS()
            if(ynDATA == True):
                dataE, dataN = tmpE, tmpN
            
            if not hasFrame:
                print("Done processing !!!")
                cv2.waitKey(3000)
                break

            yolo.getObject(frame, labelWant="", drawBox=True, bold=2, textsize=1.2, bcolor=(0,255,0), tcolor=(0,0,255))
            txt_display = ""
            if(yolo.objCounts>0 and ynDATA is True):
                defect_lists = yolo.listLabels()
                log_defect(frame_upload, frame, (dataN, dataE))
                txt_display = "發現疑似道路缺陷！"
				
            frame_desktop = desktop_bg(frame, (dataN, dataE), txt_display)
            cv2.imshow("Frame", frame_desktop )
            frame_upload = 	imutils.resize(frame_org, width=video_upload_size[0], height=video_upload_size[1])	
			
            if(write_video_out is True):
                if(video_out_type==0):
                    frame_output = cv2.resize(frame_org,cam_size,interpolation=cv2.INTER_CUBIC)
                elif(video_out_type==1):
                    frame_output = cv2.resize(frame,video_yolo_size,interpolation=cv2.INTER_CUBIC)
                elif(video_out_type==2):
                    frame_output = cv2.resize(frame_desktop,desktop_size,interpolation=cv2.INTER_CUBIC)
					
                print("SHAPE:", frame_output.shape)
                out.write(frame_output)
                if(lastE != dataE or lastN!=dataN):
                    now = datetime.datetime.now()
                    time_data = "{}{}{}{}{}{}".format(now.year,str(now.month).zfill(2),str(now.day).zfill(2),\
                        str(now.hour).zfill(2),str(now.minute).zfill(2),str(now.second).zfill(2))
                    fo.write(str(frameID) + "|" + time_data + "|" + str(dataN) + "," + str(dataE) + "\n" )

            lastE, lastN = dataE, dataN
            frameID += 1
                 
            inkey = cv2.waitKey(1)

    else:
        print("Web camera is not working.")    
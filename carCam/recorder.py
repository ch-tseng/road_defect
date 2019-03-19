#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, datetime
import cv2
import numpy as np
import imutils
from libRoad import webCam
from PIL import ImageFont, ImageDraw, Image
import serial
import signal, sys

#-----------------------------------------------
video_out = "output\\"
webcam_size  = (1920, 1080)
rotatePIC = 180
frameRate = 10.0
comPort = "COM5"   #PC的TTL2USB port
baudRate = 4800

desktop_size = (800, 480) 
desktop_frame_size = (610,344)  # video size on the desktop bg.
#-----------------------------------------------

cv2.namedWindow("Road", cv2.WND_PROP_FULLSCREEN)        # Create a named window
cv2.setWindowProperty("Road", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def desktop_bg(img, gps, txt_display1="", txt_color1=(255,0,0,0), txt_display2="", txt_color2=(255,0,0,0)):
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
    bg = printText("N: "+str(dataN), bg, color=(0,255,0,0), size=0.70, pos=(670,175), type="English")
    bg = printText("E:"+str(dataE), bg, color=(0,255,0,0), size=0.70, pos=(660,300), type="English")
    
    if(len(txt_display1)>0):
        bg = printText(txt_display1, bg, color=txt_color1, size=0.45, pos=(10,425), type="Chinese")
    if(len(txt_display2)>0):
        bg = printText(txt_display2, bg, color=txt_color2, size=0.35, pos=(350,455), type="Chinese")
		
    return bg
	
def printText(txt, bg, color=(0,255,0,0), size=0.55, pos=(0,0), type="Chinese"):
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
        #print(out)


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
    #print(gpsE, gpsN)
	
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
    bg_fresh = cv2.imread("bg.jpg")
    cam = webCam(id=0, videofile="", size=webcam_size)
    serial = serial.Serial(comPort, baudRate)
    out = ''
    dataE = dataN = "0"
    frameID = 0
    lastE, lastN = "", ""
    statusAPP = 1  #1:recoeding, 0:recording paused
	
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
            frame_org = frame.copy()
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
            #cv2.imshow("Frame", imutils.resize(frame, width=850) )

			
            if(video_out!="" and statusAPP==1):
                out.write(frame)
                if(lastE != dataE or lastN!=dataN):
                    fo.write(str(frameID) + "|" + time_data + "|" + dataN + "," + dataE + "\n" )
						
                lastE, lastN = dataE, dataN
                frameID += 1

            if(statusAPP==1):
                txt_display1 = " 錄影中: "+video_out+filename+".avi"
            elif(statusAPP==0):
                txt_display1 = " 暫停錄影: "+video_out+filename+".avi"
				
            txt_display2 = "   [CTRL+C]結束程式   [CTRL+P]暫停錄影   [CTRL+R]開始錄影"
            if(frameID % 4 == 0):
                if(statusAPP==1):
                    txtColor1 = (0,0,255,0)
                else:
                    txtColor1 = (0,0,0,0)
            else:
                txtColor1 = (0,0,0,0)				
				
            frame_desktop = desktop_bg(frame, (dataN, dataE),txt_display1 , txtColor1, txt_display2, (0,0,0,0))
            cv2.imshow("Road", frame_desktop ) 
				 
            inkey = cv2.waitKey(1)
            #print(inkey)
            if(inkey == 3):
                fo.close()
                out.release()
                #cv2.destroAllWindows()
                sys.exit()
            elif(inkey == 16):
                statusAPP = 0
            elif(inkey == 18):
                statusAPP = 1
				
    else:
        print("Web camera is not working.")	
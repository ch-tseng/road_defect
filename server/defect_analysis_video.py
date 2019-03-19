#!/usr/bin/env python
# -*- coding=utf-8 -*-

from pydarknet import Detector, Image
import cv2
import time, os, sys
import imutils

video = "/home/testvideo/20190315154845.avi"
gps_file_play = "/home/testvideo/20190315154845.gps"
map_defects = "20190315/"
rotate = 0
#----------------------------------------------------------
cfg_path = "cfg.road_server/yolov3.cfg"
weights_path = "cfg.road_server/weights/yolov3_20000.weights"
class_path = "cfg.road_server/obj.data"

defect_info_write = map_defects+"defects.log"
preview_icon_path = map_defects+"previews/"
original_path = map_defects+"originals/"
icon_preview_width = 640
#---------------------------------------------------------
if not os.path.exists(video):
    print("No such video:", video)
    sys.exit()
else:
    if not os.path.exists(gps_file_play):
        print("No gps file:", video)
        sys.exit()

if not os.path.exists(map_defects):
    os.makedirs(map_defects)

if not os.path.exists(preview_icon_path):
    os.makedirs(preview_icon_path)

if not os.path.exists(original_path):
    os.makedirs(original_path)

def obj_detect(img):
    start_time = time.time()
    img_darknet = Image(img)
    results = net.detect(img_darknet)
    end_time = time.time()

    #print("Elapsed Time:",end_time-start_time)

    x, y, w, h = 0,0,0,0
    objString = ""
    for category, score_cat, bounds in results:
        cat = category.decode("utf-8")
        sco = str(int(score_cat*100))+'%'
        #print("A:", cat, sco)
        objString += cat+"("+sco+") "
        #print("B:", objString)
        x, y, w, h = bounds
        print("cat:{}, string:{}".format(cat, objString) )
        cv2.rectangle(img, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
        cv2.putText(img, cat+'('+sco+')', (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

    #if(catString != ""):
    #print("RETURN:", objString)
    return (img, objString)
    #else:
    #    print("RETURN:", None, None, None)
    #    return (None, None, None)

def getGPS(frame_id):
    ynDATA = False
    date_time = ""
    gpsE = gpsN = 0
    for i in range(0, len(gps_frames)-1):
        if( frame_id>=int(gps_frames[i][0]) and frameID<int(gps_frames[i+1][0])):
            #print(frame_id, gps_frames[i][0], gps_frames[i][1], gps_frames[i][2])

            date_time = gps_frames[i][1]
            gpsN, gpsE = gps_frames[i][2].split(",")
            ynDATA = True

    #print("get line data:", date_time, float(gpsN), float(gpsE))

    return ynDATA, str(date_time), float(gpsE), float(gpsN)


camera = cv2.VideoCapture(video)

#load GPS data from file if play the video file
gps_frames = []
gps_file = open(gps_file_play, 'r', encoding='UTF-8')

for line in gps_file.readlines():
    gps_frame_id, time_data, gps_data = line.split("|")
    if(int(gps_frame_id)>=0):
        gps_frames.append( (int(gps_frame_id), float(time_data), gps_data) )
#--------------------------------------------------------------------------------

net = Detector(bytes(cfg_path, encoding="utf-8"), bytes(weights_path, encoding="utf-8"), 0,
               bytes(class_path, encoding="utf-8"))

f = open(defect_info_write, "a")

frameID = 0
grabbed = True
while grabbed is True:
    (grabbed, img) = camera.read()
    #print("Frame: ", frameID)

    if(grabbed is True):
        if(rotate>0):
            img = imutils.rotate_bound(img, rotate)

        yn_data, gpsTime, gpsE, gpsN = getGPS(frameID)
        frameID += 1

        if(yn_data is True):
            #print("gpsTime=",gpsTime)
            year = gpsTime[0:4]
            month = gpsTime[4:6]
            day = gpsTime[6:8]
            hour = gpsTime[8:10]
            minute = gpsTime[10:12]
            second = gpsTime[12:14]

        #try:
        (img2, obj) = obj_detect(img)
        #print("RECV:", obj)

        if obj != "":
            video_filename = os.path.basename(video)
            filename, file_extension = os.path.splitext(video_filename)
            img_filename = filename+"_"+str(frameID)
            print("{}/{}/{} {}:{}:{}|{},{}|{}|{}".format\
                (year , month , day , hour , minute , second , gpsN , gpsE, obj, img_filename + ".jpg"))
            f.write("{}/{}/{} {}:{}:{}|{},{}|{}|{}\n".format\
                (year , month , day , hour , minute , second , gpsN , gpsE, obj, img_filename + ".jpg"))

            #print(preview_icon_path+img_filename + ".jpg")
            cv2.imwrite(preview_icon_path+img_filename + ".jpg", imutils.resize(img, width=icon_preview_width))
            cv2.imwrite(original_path+img_filename + ".jpg", img)

#        except:
#            print("process {} error.".format(file))
#            pass

        time.sleep(0.5)

f.close()

#!/usr/bin/env python
# -*- coding=utf-8 -*-

from pydarknet import Detector, Image
import cv2
import time, os
import imutils

dataset_images = "defect/waiting/"
map_defects = "20190301/"
#----------------------------------------------------------
cfg_path = "cfg.road_server/yolov3.cfg"
weights_path = "cfg.road_server/weights/yolov3_20000.weights"
class_path = "cfg.road_server/obj.data"

defect_info_write = map_defects+"defects.log"
preview_icon_path = map_defects+"previews/"
original_path = map_defects+"originals/"
icon_preview_width = 90
#---------------------------------------------------------
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
        print("A:", cat, sco)
        objString += cat+":"+sco+","
        print("B:", objString)
        x, y, w, h = bounds
        #print("cat:{}, string:{}".format(cat.decode("utf-8"), catString))
        cv2.rectangle(img, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
        cv2.putText(img, cat+'('+sco+')', (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

    #if(catString != ""):
    print("RETURN:", objString)
    return (img, objString)
    #else:
    #    print("RETURN:", None, None, None)
    #    return (None, None, None)

net = Detector(bytes(cfg_path, encoding="utf-8"), bytes(weights_path, encoding="utf-8"), 0,
               bytes(class_path, encoding="utf-8"))

f = open(defect_info_write, "a")


for file in os.listdir(dataset_images):
    filename, file_extension = os.path.splitext(file)
    file_extension = file_extension.lower()

    if(file_extension == ".jpg" or file_extension==".jpeg" or file_extension==".png" or file_extension==".bmp"):
        print("Processing: ", dataset_images + file)
        info_gps = filename.split('_')
        print("length", len(info_gps))
        if(len(info_gps)==9):
            _ , gpsN, gpsE , year , month , day , hour , minute , second =\
                info_gps[0] , info_gps[1] , info_gps[2] , info_gps[3] , info_gps[4] , info_gps[5] , info_gps[6] , info_gps[7] , info_gps[8]

        try:
            img = cv2.imread(dataset_images + file)
            (img2, obj) = obj_detect(img)
            print("RECV:", obj)
            os.remove(dataset_images + file)

            if obj != "":
                img_filename = "defect_" + filename
                #print("write to ", map_defects + img_filename + ".jpg")
                #cv2.imwrite(map_defects + img_filename + ".jpg", imutils.resize(img2, width=800))
                print("{}/{}/{} {}:{}:{}|{},{}|{}|{}".format\
                    (year , month , day , hour , minute , second , gpsN , gpsE, obj, img_filename + ".jpg"))
                f.write("{}/{}/{} {}:{}:{}|{},{}|{}|{}\n".format\
                    (year , month , day , hour , minute , second , gpsN , gpsE, obj, img_filename + ".jpg"))

                cv2.imwrite(preview_icon_path+img_filename + ".jpg", imutils.resize(img, width=icon_preview_width))
                cv2.imwrite(original_path+img_filename + ".jpg", img)

        except:
            print("process {} error.".format(file))
            pass

        time.sleep(0.5)

f.close()

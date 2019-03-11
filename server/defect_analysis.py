#!/usr/bin/env python
# -*- coding=utf-8 -*-

from pydarknet import Detector, Image
import cv2
import time, os
import imutils

dataset_images = "defect/waiting/"
cfg_path = "cfg.road_server/yolov3.cfg"
weights_path = "cfg.road_server/weights/yolov3_20000.weights"
class_path = "cfg.road_server/obj.data"
defect_info_write = "20190301.defect"
map_defects = "map_defects/"
preview_icon_path = "ap_defect_icons/"
icon_preview_width = 90



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
        sco = str(score_cat)
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
            if obj != "":
                img_filename = "defect_" + filename
                print("write to ", map_defects + img_filename + ".jpg")
                cv2.imwrite(map_defects + img_filename + ".jpg", imutils.resize(img2, width=800))
                print("{}/{}/{} {}:{}:{}|{},{}|{}|{}|{}".format\
                    (year , month , day , hour , minute , second , gpsN , gpsE, obj, map_defects + img_filename + ".jpg", preview_icon_path+img_filename + ".jpg"))
                f.write("{}/{}/{} {}:{}:{}|{},{}|{}|{}|{}\n".format\
                    (year , month , day , hour , minute , second , gpsN , gpsE, obj, map_defects + img_filename + ".jpg", preview_icon_path+img_filename + ".jpg"))

                cv2.imwrite(preview_icon_path+img_filename + ".jpg", imutils.resize(img, width=icon_preview_width))

        except:
            print("process {} error.".format(file))
            pass

        time.sleep(0.5)

f.close()

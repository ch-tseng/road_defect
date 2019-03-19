import os
import numpy as np
import cv2
import imutils

spotAreas = [ [(0, 120), (960,960)], [(960, 120), (960, 960)] ]  #[(x,y), (w,h)]

source_type = 1  #0:images in a folder  1:videos in a folder
video_folder = "/media/sf_datasets/videos/road/"
img_folder = "/media/sf_datasets/images/voc/road_defection/images2/"

out_folder = "/media/sf_datasets/images/voc/road_defection/spot3/"


def chkEnv():
    if not os.path.exists(img_folder):
        print("There is no dataset folder:", img_folder)
        quit()

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
        print(out_folder + " created.")

#type = mask, cut
def spotImage(img, typeArea="mask"):

    rtnAreas = []

    for spot_area in spotAreas:

        x1 = spot_area[0][0]
        y1 = spot_area[0][1]
        w = spot_area[1][0]
        h = spot_area[1][1]
        x2 = x1 + w
        y2 = y1 + h
        print(img.shape)

        if(typeArea=="mask"):
            spot_mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")
            cv2.rectangle(spot_mask, (x1,y1), (x2,y2), 255, -1)
            print(img.shape, spot_mask.shape)
            img_processed = cv2.bitwise_and(img, img, mask = spot_mask)

        elif(typeArea=="cut"):
            img_processed = img[y1:y2, x1:x2]

        cv2.imshow("Mask", imutils.resize(img_processed, height=350))
        cv2.waitKey(1)
        rtnAreas.append(img_processed)

    return rtnAreas

#---------------------------------------------------------

chkEnv()

if(source_type==1):
    for file in os.listdir(video_folder):
        filename, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()

        if(file_extension == ".avi" or file_extension==".mp4" or file_extension==".mpg" or file_extension==".mov"):


for file in os.listdir(img_folder):
    filename, file_extension = os.path.splitext(file)
    file_extension = file_extension.lower()

    if(file_extension == ".jpg" or file_extension==".jpeg" or file_extension==".png" or file_extension==".bmp"):

        image_path = os.path.join(img_folder, file)
        img_org = cv2.imread(image_path)
        areas = spotImage(img_org, "cut")

        if(len(areas)>0):
            for i, img_spot_area in enumerate(areas):
                cv2.imwrite(os.path.join(out_folder ,str(i) + "_" + file), img_spot_area)

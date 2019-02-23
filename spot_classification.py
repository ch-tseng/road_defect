import os
import numpy as np
import cv2
import imutils

spot_area = [(260, 460), (1400,580)] #[(x,y), (w,h)]
img_folder = "/media/sf_VMshare/road_defect/"
out_folder = "/media/sf_VMshare/road_defect/spot/"


def chkEnv():
    if not os.path.exists(img_folder):
        print("There is no dataset folder:", img_folder)
        quit()

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
        print(out_folder + " created.")

#type = mask, cut
def spotImage(img, typeArea="mask"):
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

    cv2.imshow("Mask", imutils.resize(img_processed, height=450))
    cv2.waitKey(0)

    return img_processed

#---------------------------------------------------------

chkEnv()

for file in os.listdir(img_folder):
    filename, file_extension = os.path.splitext(file)
    file_extension = file_extension.lower()

    if(file_extension == ".jpg" or file_extension==".jpeg" or file_extension==".png" or file_extension==".bmp"):

        image_path = img_folder + file
        img_org = cv2.imread(image_path)
        spotImage(img_org, "cut")

import time
import imutils
import cv2
import numpy as np

class webCam:
    def __init__(self, id, size=(320, 240)):
        self.cam = cv2.VideoCapture(id)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    def working(self):
        webCam = self.cam
        if(webCam.isOpened() is True):
            return True
        else:
            return False

    def camRealSize(self):
        webcam = self.cam
        width = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)
		
    def takepic(self, rotate=0, vflip=False, hflip=False, resize=None, savePath=None):
        webcam = self.cam
        hasFrame, frame = webcam.read()

        if(vflip==True):
            frame = cv2.flip(frame, 0)
        if(hflip==True):
            frame = cv2.flip(frame, 1)

        if(rotate>0):
            frame = imutils.rotate(frame, rotate)
        if(resize is not None):
            frame = imutils.resize(frame, size=resize)
        if((hasFrame is True) and (savePath is not None)):
            cv2.imwrite(savePath+str(time.time())+".jpg", frame)

        return hasFrame, frame

    def release(self):
        webcam = self.cam
        webcam.release()
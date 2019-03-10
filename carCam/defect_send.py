#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys, time, os
import socket  # Import socket module
import cv2
import imutils

host = "sam.bim-group.com"  #Ip address that the TCPServer  is there
port = 8021                     # Reserve a port for your service every new transfer wants a new port or you must wait.
defect_org_path = "defect\\original\\"

def send_file(gpsData, org_img_path ):
    print('Send filename.')
    filename = str.encode(gpsData)
    s.send(filename)
	
    print('Send defect image.')
    f = open(org_img_path,'rb')
    l = f.read(2048)	
    while (l):
       s.send(l)
       print('Sent ',repr(l))
       l = f.read(2048)
    f.close()

if __name__ == "__main__":
	
    for file in os.listdir(defect_org_path):
        try:
            s = socket.socket()             # Create a socket object
            s.connect((host, port))

        except socket.error as msg:
            print(msg)
            sys.exit(1)
		
        filename, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()
		
        if(file_extension == ".jpg" or file_extension==".jpeg" or file_extension==".png" or file_extension==".bmp"):
            send_file(filename, defect_org_path + file )

        s.close()
        print('connection closed')
        os.remove(defect_org_path + file)
        time.sleep(1)
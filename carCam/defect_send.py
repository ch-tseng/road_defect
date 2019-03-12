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

    filename = str.encode(gpsData)
    send_status = False
	
    try:
        print('Send filename.')	
        s.send(filename)
    except:
        print("Send filename.... got error.")
        return False

    f = open(org_img_path,'rb')
    l = f.read(1024)
    try:		
        print('Send defect image.')
        while (l):
           s.send(l)
           print('Sent ',repr(l))
           l = f.read(1024)
        f.close()
        return True

    except:
        f.close()
        print("Send image.... got error.")
        return False
		
if __name__ == "__main__":
    conn_status = False
    while True:	
        for id, file in enumerate(os.listdir(defect_org_path)):
            print(id, "Uploading image:", file)
            while conn_status is False:
                try:
                    s = socket.socket()             # Create a socket object
                    s.connect((host, port))
                    conn_status = True

                except socket.error as msg:
                    print(msg)
                    #sys.exit(1)
                    conn_status = False
                    pass
				
            filename, file_extension = os.path.splitext(file)
            file_extension = file_extension.lower()
		
            if(file_extension == ".jpg" or file_extension==".jpeg" or file_extension==".png" or file_extension==".bmp"):
                upload_status = send_file(filename, defect_org_path + file )

            s.close()
            conn_status = False
            print('connection closed')
            if(upload_status is True):
                try:
                    os.remove(defect_org_path + file)
                except:
                    pass
					
            time.sleep(1)
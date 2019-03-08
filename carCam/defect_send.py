#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
import socket                   # Import socket module

try:
    s = socket.socket()             # Create a socket object
    host = "sam.bim-group.com"  #Ip address that the TCPServer  is there
    port = 8021                     # Reserve a port for your service every new transfer wants a new port or you must wait.

    s.connect((host, port))
    s.send("GPS (24.2323,211.5325708)")

except socket.error as msg:
    print(msg)
    sys.exit(1)

filename='../../test.jpg' #In the same folder or path is this file running must the file you want to tranfser to be
f = open(filename,'rb')
l = f.read(1024)

while (l):
   s.send(l)
   print('Sent ',repr(l))
   l = f.read(1024)

f.close()
print('Done sending')

s.close()
print('connection closed')

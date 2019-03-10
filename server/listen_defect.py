#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket                   # Import socket module

port = 8021                    # Reserve a port for your service every new transfer wants a new port or you must wait.
recv_save_path = "defect/waiting/"


#--------------------------------------------
s = socket.socket()             # Create a socket object
host = ""   # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print ('Server listening....')


while True:
    conn, addr = s.accept()     # Establish connection with client.
    print ('Got connection from', addr)
    filename_recv = conn.recv(1024)
    filename = filename_recv.decode("utf-8")
    print("RECV filename:", filename)

    with open(recv_save_path+filename+'.jpg', 'wb') as f:
        print("RECV Defect:", filename)
        data = conn.recv(1024)
        while data:
            f.write(data)
            print('receiving data...')
            data = conn.recv(1024)
            #print('data=%s', (data))
            if not data:
                break
        f.close()
        conn.close()

        print('Done receiving')

s.close()

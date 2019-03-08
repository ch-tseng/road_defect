#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket                   # Import socket module

port = 8021                    # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()             # Create a socket object
host = ""   # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print ('Server listening....')


while True:
    conn, addr = s.accept()     # Establish connection with client.
    #print ('Got connection from', addr)
    #print("RECV GPS:", conn.recv(1024))

    with open('test.jpg', 'wb') as f:
        print ('Got connection from', addr)
        print("RECV GPS:", conn.recv(1024))

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


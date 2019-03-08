import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = "sam.bim-group.com"  #Ip address that the TCPServer  is there
port = 8021                     # Reserve a port for your service every new transfer wants a new port or you must wait.

s.connect((host, port))
#s.send("Hello server!")

filename='test.jpg' #In the same folder or path is this file running must the file you want to tranfser to be
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

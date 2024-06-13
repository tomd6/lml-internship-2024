from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys

PORT_NUMBER = 5331
SIZE = 1024
endOfConnection = b'<endOfConnection>'
hostName = gethostbyname('0.0.0.0')

mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.bind((hostName, PORT_NUMBER))

print ("Test server listening on port {0}\n".format(PORT_NUMBER))

image = open("Image.jpg", "wb")

(data, addr) = mySocket.recvfrom(SIZE)
while data:
    mySocket.sendto(b"receved", addr)
    image.write(data)
    (data, addr) = mySocket.recvfrom(SIZE)

image.close()
sys.exit()
# !/usr/bin/env python3

from pyniryo2 import *
import cv2
import numpy as np
from math import pi
import sys
from socket import socket, AF_INET, SOCK_DGRAM

SERVER_IP = '172.17.135.191'
PORT_NUMBER = 5331
SIZE = 1024

print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket(AF_INET, SOCK_DGRAM)


ned = NiryoRobot("localhost")
ned.arm.calibrate_auto()
ned.arm.move_joints([0,0,-0.5,0,-1.3,0])
mySocket.sendto(b"move the red cube next to the blue cube", (SERVER_IP, PORT_NUMBER))

with open("Image.jpg", "wb") as f:
        f.write(ned.vision.get_img_compressed.value)

    
image = open("Image.jpg", "rb")
chunck = image.read(SIZE)

while chunck:
    mySocket.sendto(chunck, (SERVER_IP, PORT_NUMBER))
    chunck = image.read(SIZE)

mySocket.sendto(b"end_img", (SERVER_IP, PORT_NUMBER))



(data,addr) = mySocket.recvfrom(SIZE)
while data != b'end':
    print(data)
    data = data.decode("utf-8").split()
    print(data)
    moves = [float(i) for i in data]
    print(moves)
    ned.arm.move_joints(moves[0:-1])

    with open("Image.jpg", "wb") as f:
        f.write(ned.vision.get_img_compressed.value)

    

    """for i in range(0,len(ned.vision.get_img_compressed.value),SIZE):
        chunck = ned.vision.get_img_compressed.value[i:i+SIZE]
        mySocket.sendto(chunck, (SERVER_IP, PORT_NUMBER))"""
    image = open("Image.jpg", "rb")
    chunck = image.read(SIZE)
    mySocket.sendto(b"move the red cube next to the blue cube", (SERVER_IP, PORT_NUMBER))

    while chunck:
        mySocket.sendto(chunck, (SERVER_IP, PORT_NUMBER))
        chunck = image.read(SIZE)
    
    
    image.close()
    mySocket.sendto(b"end_img", (SERVER_IP, PORT_NUMBER))
    (data, addr) = mySocket.recvfrom(SIZE)

sys.exit()



image = open("Image.jpg", "rb")
chunck = image.read(SIZE)

while chunck:
    mySocket.sendto(chunck, (SERVER_IP, PORT_NUMBER))
    chunck = image.read(SIZE)
    (data, addr) = mySocket.recvfrom(SIZE)
    print(data.decode("utf-8"))

image.close()
sys.exit()
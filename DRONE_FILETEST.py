
import cv2
import numpy as np
from math import sqrt

def is_square(apositiveint):
  x = apositiveint // 2
  seen = set([x])
  while x * x != apositiveint:
    x = (x + (apositiveint // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True

def crop2(infile,imgheight,imgwidth,imgheight2, imgwidth2):
    #im = Image.open(infile)
    #imgwidth, imgheight = im.size
    b= []
    for i in range(imgheight//imgheight2):
        for j in range(imgwidth//imgwidth2):
            crop_img = infile[i*imgheight2:(i+1)*imgheight2, j*imgwidth2:(j+1)*imgwidth2]
            b.append(crop_img)
    return b

def crop(im, k):
    k2 = 9

    boolean_var = is_square(k)
    #im = Image.open(input)
    # 290 , 640
    imgheight, imgwidth, chan = im.shape

    imgheight = int(imgheight - (imgheight % sqrt(k)))
    imgwidth = int(imgwidth - (imgwidth % sqrt(k)))

    imgheight2 = int(int(imgheight - (imgheight % sqrt(k))) / 3)
    imgwidth2 = int(int(imgwidth - (imgwidth % sqrt(k))) / 3)



image_grid_array = []
size_of_grid = 9
grid_length = 3
image = cv2.imread("test_img.jpeg")

Ps = 0
Pl = .5
Pr = .2

i = 1

file = open('DroneRead.txt', 'w+')
file.write("1")
droneRead = '0'
file.close()

while(True):

    canRead = '0'
    # Test for I/O file close permissions
    while canRead == "0":

        file = open('canRead.txt', 'w+')
        file.write("1")
        file.close()
        file = open('canRead.txt', 'r+')
        canRead = str(file.readline())
        print "Can Read Succeeded to make 1"

        file.close()

# To run this in python 3.5 we will need to run a script that uses the "env"
# wrapper
# Once the pipeline is established, have the thread continuousely generate new samples
#
# can definitely recursion this size_of grid /2 + 1

    while(droneRead != '1'):

        file = open('DroneRead.txt', 'r')
        droneRead = str(file.readline())
        file.close()

    while (droneRead == '1'):

        try:

            file = open('out.txt', 'r')
            collision = float(file.readline().split(":")[1])
            print("COLLISION: " + str(collision))
            file.close()
        except:
            collision = 0
            print("COLLISION: -1" )

        file = open('DroneRead.txt', 'w+')
        file.write("0")
        droneRead = str(file.readline())

        file.close()

        print("Drone Read inactive")


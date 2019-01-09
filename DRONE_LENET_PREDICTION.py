from keras.preprocessing.image import img_to_array
import cv2
import numpy as np
from math import sqrt
from keras.models import load_model

file = open('canRead.txt', 'w+')
canRead = file.write('0')
file.close()

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



model = load_model(r"C:\Users\Sean\Drive_by_Ryan_Gosling\The_Og\drone_project\model\model_min.hdf5")




import sys
while(True):
    W, H = 213, 96
    file = open('canRead.txt', 'r')
    canRead = file.readline()
    file.close()
    if canRead == '1':
        image = cv2.imread("test_img.jpeg")
                        # classify the input image
        image = cv2.resize(image, (W, H))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        (notcollision, collision) = model.predict(image)[0]

        file = open('out.txt', 'w+')
        file.write("COLLISION:" + str(collision))
        file.close()

        file = open('canRead.txt', 'w')
        file.write("0")
        file.close()

        file = open('DroneRead.txt', 'w')
        canRead = file.write("1")
        file.close()



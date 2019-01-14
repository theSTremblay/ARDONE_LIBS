"""\
Demo app for the ARDrone.
This simple application allows to control the drone and see the drone's video
stream.
Copyright (c) 2011 Bastian Venthur
The license and distribution terms for this file may be
found in the file LICENSE in this distribution.
"""

# THis demo is to prove the ability of the drone to move towards a destination, the parameters will bbe a point to move towards and the drone must do its best to get there.
import pygame

from pydrone import libardrone
import cv2
import time

from math import sqrt
import numpy as np
from Destination_Pathing import *


#3e^(-.5x)
def expoential_time_decay(current_time_dif):
   time_of_flag = 3* np.exp(-.5 * current_time_dif)

   if time_of_flag > 1:
       return True
   else:
       return False


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



if __name__ == '__main__':
    pygame.init()
    cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
    current_time = time.time()

    current_point = Point(0,0)
    destination_point = Point(5,0)

    left_flag = time.time()
    right_flag = time.time()

    running2 = True
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    clock = pygame.time.Clock()
    # test this for phi values which gives rotation
    test = drone.navdata[0]
    current_angle = test
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                drone.hover()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drone.reset()
                    running = False
                # takeoff / land
                elif event.key == pygame.K_RETURN:
                    drone.takeoff()
                    current_angle = GPS_pathing(current_point, destination_point, False, False, drone)
                elif event.key == pygame.K_SPACE:
                    drone.land()
                # emergency
                elif event.key == pygame.K_BACKSPACE:
                    current_angle = GPS_pathing(current_point, destination_point, False, False, drone)
                    #drone.reset()
                # forward / backward
                elif event.key == pygame.K_w:
                    drone.move_forward()
                elif event.key == pygame.K_s:
                    drone.move_backward()
                # left / right
                elif event.key == pygame.K_a:
                    drone.move_left()
                elif event.key == pygame.K_d:
                    drone.move_right()
                # up / down
                elif event.key == pygame.K_UP:
                    drone.move_up()
                elif event.key == pygame.K_DOWN:
                    drone.move_down()
                # turn left / turn right
                elif event.key == pygame.K_LEFT:
                    drone.turn_left()
                elif event.key == pygame.K_RIGHT:
                    drone.turn_right()
                # speed
                elif event.key == pygame.K_1:
                    drone.speed = 0.1
                elif event.key == pygame.K_2:
                    drone.speed = 0.2
                elif event.key == pygame.K_3:
                    drone.speed = 0.3
                elif event.key == pygame.K_4:
                    drone.speed = 0.4
                elif event.key == pygame.K_5:
                    drone.speed = 0.5
                elif event.key == pygame.K_6:
                    drone.speed = 0.6
                elif event.key == pygame.K_7:
                    drone.speed = 0.7
                elif event.key == pygame.K_8:
                    drone.speed = 0.8
                elif event.key == pygame.K_9:
                    drone.speed = 0.9
                elif event.key == pygame.K_0:
                    drone.speed = 1.0

        try:

            image_grid_array = []
            size_of_grid = 9
            grid_length = 3

            try:
                frame = None

                while running2:
                    # get current frame of video
                    running2, frame = cam.read()
                    if running2:
                        cv2.imshow('frame', frame)
                        image_grid_array.extend(crop(frame, size_of_grid))

                        Ps = 0
                        Pl = .5
                        Pr = .2

                        i = 1

                        file = open('DroneRead.txt', 'w+')
                        file.write("1")
                        droneRead = 0
                        file.close()

                        for image in image_grid_array:

                            cv2.imwrite("test_img.jpeg", image)

                            canRead = '0'
                            # Test for I/O file close permissions
                            while canRead == "0":
                                file = open('canRead.txt', 'w+')
                                file.write("1")
                                file.close()
                                file = open('canRead.txt', 'r+')
                                canRead = str(file.readline())
                                print
                                "Can Read Succeeded to make 1"

                                file.close()

                                # To run this in python 3.5 we will need to run a script that uses the "env"
                                # wrapper
                                # Once the pipeline is established, have the thread continuousely generate new samples
                                #
                                # can definitely recursion this size_of grid /2 + 1

                            while (droneRead != '1'):
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
                                    print("COLLISION: -1")

                                file = open('DroneRead.txt', 'w+')
                                file.write("0")
                                droneRead = str(file.readline())

                                file.close()

                                print("Drone Read inactive")

                            if i % grid_length < (size_of_grid / 2 + 1):
                                Pl += collision
                            elif i % grid_length == (size_of_grid / 2 + 1):
                                Ps += collision
                            else:
                                Pr += collision

                        event = 1

                        print("Probability Right = " + str(Pr))
                        print("PRobabiltity Left = ") + str(Pl)
                        print("PRobabiltity Straight = ") + str(Ps)
                        # forward / backward
                        if Pr and Pl > Ps:

                            # Assume in 0.2 seconds the drones linear speed moves the drone approx
                            # 1 foot. This is about 3.5 mph


                            drone.move_forward()
                            time.sleep(0.2)

                            drone.halt()
                            x = 1* math.cos(current_angle) + current_point.x
                            y = 1 * math.sin(current_angle) + current_point.y
                            current_point = Point(x, y)

                        else:
                            left_time_dif = time.time() - left_flag
                            left_check = expoential_time_decay(left_time_dif)

                            right_time_dif = time.time() - right_flag
                            right_check = expoential_time_decay(right_time_dif)
                            if Pr <= Pl and left_check == True:

                                drone.move_left()
                                time.sleep(0.2)

                                drone.halt()
                                current_angle = drone.navdata[0]

                            elif Pr > Pl and right_check == True:
                                drone.move_right()
                                current_angle = drone.navdata[0]
                                time.sleep(0.2)

                                drone.halt()
                                current_angle = drone.navdata[0]
                                # turn left / turn right
                            else:
                                drone.halt()
                                flip(drone, current_angle,180)
                    else:
                        # error reading frame
                        print 'error reading video feed'
            except Exception as e:
                print(e)



            hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
            bat = drone.navdata.get(0, dict()).get('battery', 0)
            f = pygame.font.Font(None, 20)
            hud = f.render('Battery: %i%%' % bat, True, hud_color)
            screen.blit(hud, (10, 10))
        except:
            pass

        pygame.display.flip()
        clock.tick()
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    print "Shutting down...",
    drone.halt()
    print "Ok."
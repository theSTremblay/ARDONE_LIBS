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


if __name__ == '__main__':
    pygame.init()
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    clock = pygame.time.Clock()
    # test this for phi values which gives rotation
    test = drone.navdata[0]
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
                elif event.key == pygame.K_SPACE:
                    drone.land()
                # emergency
                elif event.key == pygame.K_BACKSPACE:
                    drone.reset()
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

                            # forward / backward
                            if Pr and Pl > Ps:

                                drone.move_forward()
                            else:
                                if Pr <= Pl:

                                    drone.move_left()
                                else:
                                    drone.move_right()
                                    # turn left / turn right
                        else:
                            # error reading frame
                            print 'error reading video feed'
                except Exception as e:
                    print(e)

                hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (
                10, 10, 255)
                bat = drone.navdata.get(0, dict()).get('battery', 0)
                f = pygame.font.Font(None, 20)
                hud = f.render('Battery: %i%%' % bat, True, hud_color)
                screen.blit(hud, (10, 10))
            except Exception as e:
                print(str(e))
                pass
            hud_color = (10, 10, 255)
            if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1):
                hud_color = (255, 0, 0)
            bat = drone.navdata.get(0, dict()).get('battery', 0)
            f = pygame.font.Font(None, 20)
            hud = f.render('Battery: %i%%' % bat, True, hud_color)
            screen.blit(surface, (0, 0))
            screen.blit(hud, (10, 10))
        except:
            pass

        pygame.display.flip()
        clock.tick()
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    print "Shutting down...",
    drone.halt()
    print "Ok."
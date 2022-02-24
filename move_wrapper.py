import picar_4wd as fc
import time
import math
import numpy as np

POWER = 100
ONE_DEGREE = 1.2 / 180
ONE_CENTIMETER = .6 / 30


end_point = (-30, 30)

angle = math.degrees(math.atan(end_point[0] / end_point[1]))


def move_amt(cm):
    fc.forward(POWER)
    time.sleep(ONE_CENTIMETER * cm)
    print("Moving {} cm".format(cm))
    fc.stop()

def turn(cur_angle, new_angle):
    angle_dif = new_angle - cur_angle
    circle_dif = 360 - angle_dif
    print(circle_dif)
    if circle_dif < 180:
        fc.turn_left(POWER)
        print("Turning {} degrees left".format(circle_dif))
        time.sleep(abs(ONE_DEGREE * circle_dif))
    else:
        if angle_dif < 0:
            angle_dif = 360 + angle_dif
        fc.turn_right(POWER)
        print("Turning {} degrees right".format(angle_dif))
        time.sleep(abs(ONE_DEGREE * angle_dif))
    
    fc.stop()
    
    
    

def move_to_coordinate(end_point):
    angle = math.degrees(math.atan(end_point[0] / end_point[1]))

    if angle > 0:
        fc.turn_right(POWER)
    else:
        fc.turn_left(POWER)
    
    time.sleep(abs(angle) * ONE_DEGREE)
    print(abs(angle) * ONE_DEGREE)
    fc.stop()

    dist = np.sqrt(end_point[0]**2 + end_point[1]**2)

    fc.forward(POWER)
    time.sleep(ONE_CENTIMETER * dist)
    print(ONE_CENTIMETER * dist)
    fc.stop()



if __name__ == "__main__":
    # fc.stop()
    move_to_coordinate((-30, 30))
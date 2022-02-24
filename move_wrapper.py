from chardet import detect
import picar_4wd as fc
import time
import math
import numpy as np
from detect_stop import detect_stop

POWER = 100
ONE_DEGREE = 1.2 / 180
ONE_CENTIMETER = .6 / 30
MOVE = False


end_point = (-30, 30)

angle = math.degrees(math.atan(end_point[0] / end_point[1]))

# Moves the car a given amt of centimeters
def move_amt(cm):
    if MOVE:
        fc.forward(POWER)
    print("Moving {} cm".format(cm))
    detect_stop(ONE_CENTIMETER * cm)
    fc.stop()

# Turn the car from a current angle to a new angle.
# Checks for stops while moving
def turn(cur_angle, new_angle):
    # Calculate 180 behind car angle
    new_behind = 180 + angle 
    if new_behind > 360:
        new_behind -= 360
    
    # Angle and direction
    turn = (0, 'r')

    # Check if above or below x-axis, elinate possibilities
    if cur_angle < 180:
        if new_angle > cur_angle and new_angle < new_behind:
            turn = (new_angle - cur_angle, 'r')
        elif new_angle < cur_angle:
            turn = (cur_angle - new_angle, 'l')
        else:
            turn = (cur_angle + (360 - new_angle), 'l')
    else:
        if new_angle < cur_angle and new_angle > new_behind:
            turn = (cur_angle - new_angle, 'l')
        elif new_angle > cur_angle:
            turn = (new_angle - cur_angle, 'r')
        else:
            turn = (new_angle + (360 - cur_angle), 'r')

    print(turn)
    if turn[1] == 'r' and MOVE:
        fc.turn_right(POWER)
    elif MOVE:
        fc.turn_left(POWER)

    detect_stop(ONE_DEGREE * turn[0])

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
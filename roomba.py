import picar_4wd as fc
from picar_4wd.ultrasonic import Ultrasonic 
import time
import random
POWER = 100

def move25():
    speed4 = fc.Speed(25)
    speed4.start()

    fc.backward(100)
    x = 0
    for i in range(10):
        time.sleep(0.1)
        speed = speed4()
        x += speed * 0.1
        print("%smm/s"%speed)
    print("%smm"%x)
    speed4.deinit()
    fc.stop()


def roomba():
    distance = fc.get_distance_at(0)
    fc.forward(POWER)

    # print(distance)
    while True:
        fc.forward(POWER)
        while(distance > 10):
            distance = fc.get_distance_at(0)
            # print(distance)
        fc.backward(20)
        time.sleep(1)
        turn_val = random.randint(0, 1)

        if (turn_val == 0):
            fc.turn_left(POWER)
        else:
            fc.turn_right(POWER)
        time.sleep(.6)
        fc.stop()
        distance = fc.get_distance_at(0)


fc.stop()

# roomba()

import RPi.GPIO as GPIO
from time import sleep
import chess
from concurrent import futures
from pypose.ax12 import *
from pypose.driver import Driver
#from raspberryturk.embeedded.motion.gripper_movement_engine import GripperMovementEngine

BIN_NUM = {0: 31, 1: 33, 2: 35, 3: 37}  # map digit to gpio pins

RANK_NUM = {"h":[0,0,0,0],"g":[0,0,0,1],"f":[0,0,1,0],"e":[0,0,1,1],"d":[0,1,0,0],"c":[0,1,0,1],"b":[0,1,1,0],
           "a":[0,1,1,1],"ob1":[1,0,0,0], "ob2":[1,0,0,1], "ob3":[1,0,1,0], "ob4":[1,0,1,1], "r1":[1,1,0,0],
            "r2":[1,1,0,1], "r3":[1,1,1,0], "r4":[1,1,1,1],}
OUTPUT = {0:GPIO.LOW, 1:GPIO.HIGH}

def op(item):
    try:
        GPIO.output(BIN_NUM[item], OUTPUT[item])
    except:
        print('cant print terminal dummy')

class Slider(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        for key in BIN_NUM.keys():
            GPIO.setup(BIN_NUM[key], GPIO.OUT)

    def move_to_rank(self, rank):
        temp_list = RANK_NUM[rank] ## MULTI PROCESSING TO SEND GPIO SIGNALS AT SAME TIME
        executor = futures.ProcessPoolExecutor(4)
        fut = [executor.submit(op, i) for i in range(0,len(temp_list))]
        futures.wait(fut)

    def cleanup(self):
        GPIO.cleanup()

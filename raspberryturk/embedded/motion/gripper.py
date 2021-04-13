import RPi.GPIO as GPIO
from time import sleep
import chess
from pypose.ax12 import *
from pypose.driver import Driver

electromagnet_pin = 40
servo_pin = 38

PIECE_HEIGHTS = {
    chess.KING: 97,
    chess.QUEEN: 75,
    chess.ROOK: 46,
    chess.BISHOP: 65,
    chess.KNIGHT: 58,
    chess.PAWN:45
}

PIECE_WIDTHS = {
    chess.KING: 22,
    chess.QUEEN: 24,
    chess.ROOK: 22,
    chess.BISHOP 18,
    chess.KNIGHT: 10,
    chess.PAWN: 14
}

MAX_PIECE_HEIGHT = max(PIECE_HEIGHTS.values())
RESTING_HEIGHT = MAX_PIECE_HEIGHT + 15
SPEED = 5

class Gripper(object):
    def __init__(self, port="/dev/ttyUSB0"):
        self.driver = Driver(port=port)

    def close(self):
        self.driver.close()

    def mm_to_bytes(length):
        # Some code that scales the grip width to bytes

    # Opens gripper fully, index value may be incorrect
    def open_gripper(self, speed):
        self.driver.setReg(4, P_GOAL_SPEED_L, [speed[i%2]%256, speed[i%2]>>8])
        self.driver.setReg(4, P_GOAL_POSITION_L, [511, 525])

    def move(self, piece_type, speed):
        piece_width = PIECE_WIDTHS[piece_type]
        self.driver.setReg(4, P_GOAL_SPEED_L, [speed[i%2]%256, speed[i%2]>>8])
        self.driver.setReg(4, P_GOAL_POSITION_L, [mm_to_bytes(piece_width - 20), mm_to_bytes(piece_width + 20)])

    def grab_piece(self, piece_type):
        self.move(piece_type, [SPEED, SPEED])

    def dropoff_piece(self):
        self.open_gripper([SPEED, SPEED])
        

    '''
    def __init__(self):
        self.previous_z = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo_pin, GPIO.OUT)
        GPIO.setup(electromagnet_pin, GPIO.OUT)

    def calibrate(self):
        self.move(RESTING_HEIGHT)

    def move(self, z):
        z = max(0.0, min(z, 100.0))
        dc = (z * 0.067) + 4.0
        p = GPIO.PWM(servo_pin, 50.0)
        p.start(dc)
        if self.previous_z is None:
            t = 10.0
        else:
            t = (abs(self.previous_z - z) / 10.0) + 0.5
        sleep(t)
        p.stop()
        del p
        self.previous_z = z

    def electromagnet(self, on):
        output = GPIO.HIGH if on else GPIO.LOW
        GPIO.output(electromagnet_pin, output)

    def pickup(self, piece_type):
        piece_height = PIECE_HEIGHTS[piece_type]
        self.move(piece_height)
        sleep(0.4)
        self.electromagnet(True)
        sleep(0.2)
        self.move(RESTING_HEIGHT + piece_height)

    def dropoff(self, piece_type):
        piece_height = PIECE_HEIGHTS[piece_type]
        self.move(piece_height)
        sleep(0.2)
        self.electromagnet(False)
        sleep(0.4)
        self.move(RESTING_HEIGHT)

    def cleanup(self):
        GPIO.cleanup()
    '''

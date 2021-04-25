import time
import serial
import numpy as np
from pytweening import easeInOutQuint, easeOutSine
from scipy.misc import derivative
from scipy.interpolate import interp1d
from raspberryturk.embedded.motion.arm_movement_engine import ArmMovementEngine
from pypose.ax12 import *
from pypose.driver import Driver

## MAKE SURE TO CHANGE THESE VALUES WHEN TESTING THE ARM OR ELSE POTENTIAL DISASTER
SERVO_1 = 4
MIN_SPEED = 300
MAX_SPEED = 300
RESTING_POSITION = 512

# Converts the registers bytes to the base 10 value of the register
def _register_bytes_to_value(register_bytes):
    #print register_bytes

    return register_bytes[0] + (register_bytes[1] << 8)

# Takes derivative of easeInOutQuint at x0 = p
def _easing_derivative(p):
    d = 0.0
    try:
        d = derivative(easeInOutQuint, p, dx=1e-6)
    except ValueError:
        pass
    return d

# Given the start position, current position, and goal position, adjusts the speed of the arm
def _adjusted_speed(start_position, goal_position, position):
    r = np.array([start_position, goal_position])
    clipped_position = np.clip(position, r.min(), r.max())  # Clip keeps the position in the defined range
    f = interp1d(r, [0,1])  #interpolates a 1D function
    adj = _easing_derivative(f(clipped_position)) / _easing_derivative(0.5) 
    amp = easeOutSine(abs(goal_position - start_position) / 1023.0)
    return np.int(MIN_SPEED + (MAX_SPEED - MIN_SPEED) * adj * amp)

# Creates a class for the arm object
class Gripper(object):
    def __init__(self, port="/dev/tty.usbserial-AR0JW21B"): ## CHANGE PORT
        self.driver = Driver(port=port)
        self.movement_engine = ArmMovementEngine()

    #Closes the window the driver has control of
    def close(self):
        self.driver.close()

    #Recenters the arm to its starting position
    def recenter(self):
        self.move(512)

    def grip(self):
        self.move(900)

    def release(self):
        self.move(512)

    #Moves arm to its rest position
    def return_to_rest(self):
        self.move_to_point([20, 13.5])

    #Moves arm to correct position
    def move(self, goal_position):
        #print(goal_position)
        time.sleep(0.2)
        start_position = self.current_position()
        #print(start_position)
        self.set_speed(MIN_SPEED)

        self.driver.setReg(SERVO_1, P_GOAL_POSITION_L, [goal_position%256, goal_position>>8])
        while self._is_moving():
            position = self.current_position()
            speed = _adjusted_speed(start_position, goal_position, position)
            self.set_speed(speed)

    #Determines where robot needs to move
    def move_to_point(self, pt):
        goal_position = self.movement_engine.convert_point(pt)
        self.move(goal_position)

    #Sets the speed of the servos
    def set_speed(self, speed):
        self.driver.setReg(SERVO_1, P_GOAL_SPEED_L, [speed%256, speed>>8])

    #Returns the current position of the servo
    def current_position(self):
        #print(self._values_for_register(P_PRESENT_POSITION_L))
        return self._values_for_register(P_PRESENT_POSITION_L)

    #Checks if the servos are moving
    def _is_moving(self):
        return self.driver.getReg(SERVO_1, P_MOVING, 1) == 1

    #Returns the value in specified register
    def _values_for_register(self, register):
        #for i in range(250,256):
        #    ret = self.driver.getReg(i, register, 2)
        #    if ret == -1:
        #        print(str(i) + "wrong id")
        #    else:
        #        print(ret)
        #        print(str(i) + " IS THE SERVO ID")
        #        break
        return _register_bytes_to_value(self.driver.getReg(SERVO_1, register, 2))
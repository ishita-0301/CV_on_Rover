"""L298N differential drive, driven straight from the rover Pi's GPIO.

Uses gpiozero's Motor, which handles the IN1/IN2 direction pins plus the enable
pin per bank. The six rocker-bogie wheels are ganged into a left and a right
bank; steering is differential (spin the banks in opposite directions).

gpiozero only runs on a Raspberry Pi, so importing this module elsewhere will
fail - that is expected; it is rover-Pi code.
"""

from gpiozero import Motor

import config


class Rover:
    def __init__(self):
        self.left = Motor(
            forward=config.LEFT_FORWARD,
            backward=config.LEFT_BACKWARD,
            enable=config.LEFT_ENABLE,
        )
        self.right = Motor(
            forward=config.RIGHT_FORWARD,
            backward=config.RIGHT_BACKWARD,
            enable=config.RIGHT_ENABLE,
        )
        self.speed = config.DRIVE_SPEED

    def forward(self):
        self.left.forward(self.speed)
        self.right.forward(self.speed)

    def backward(self):
        self.left.backward(self.speed)
        self.right.backward(self.speed)

    def turn_left(self):
        # pivot left: left bank reverses, right bank drives forward
        self.left.backward(self.speed)
        self.right.forward(self.speed)

    def turn_right(self):
        self.left.forward(self.speed)
        self.right.backward(self.speed)

    def stop(self):
        self.left.stop()
        self.right.stop()

    def close(self):
        self.stop()
        self.left.close()
        self.right.close()

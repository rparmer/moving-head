import logging
import os
from gpiozero import Servo
from time import sleep

os.environ['GPIOZERO_PIN_FACTORY'] = 'pigpio'

class ServoController():
    def __init__(self, gpip_pin = 17):
        logging.info('Setting up servo controller')
        self.gpip_pin = gpip_pin
        self.servo = None
        self._setup_servo()

    def __del__(self):
        logging.info('Cleaning up servo controller')
        self.reset_to_center()
        if self.servo:
            self.servo.close()

    def _setup_servo(self):
        self.servo = Servo(self.gpip_pin)
        self.reset_to_center()

    def _verify_value(self, value):
        if value > 1:
            return 1
        if value < -1:
            return -1
        return round(value, 2)
    
    def set_servo_position(self, value):
        current_value = self.servo.value
        target_value = self._verify_value(value)

        # incrementally change the position to
        # prevent the head from moving too quickly
        while current_value != target_value:
            if current_value < target_value:
                current_value += 0.01
            else:
                current_value -= 0.01
            current_value = self._verify_value(current_value)
            self.servo.value = current_value
            sleep(0.01)

    def reset_to_center(self):
        self.set_servo_position(0)

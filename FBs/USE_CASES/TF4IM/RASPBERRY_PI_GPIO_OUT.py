"""
This block takes a GPIO PIN Number (Board numbering scheme)
and returns the DIGITAL level of the PIN.
"""
import RPi.GPIO as GPIO
import time

class RASPBERRY_PI_GPIO_OUT:

    def __init__(self):
        self.pin_number = None
        self.result = None
        GPIO.setmode(GPIO.BOARD)

    def schedule(self, event_name, event_value,
                 pin_number, value):

        if event_name == 'INIT':
            self.pin_number = pin_number
            GPIO.setup(pin_number, GPIO.OUT)
            return [event_value, None]

        elif event_name == 'READ':
            time.sleep(0.20)
            GPIO.output(pin_number, bool(value))
            return [None, event_value]
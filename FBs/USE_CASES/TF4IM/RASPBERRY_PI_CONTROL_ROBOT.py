"""
This block takes a GPIO PIN Number (Board numbering scheme)
and if the button is pressed before timeout, FIRST_CONDITION is triggered.
SECOND condition is triggered if the button is not pressed befpre timeout.

ATENTION INVERSE LOGIC (because of the Arduino firmware used at the time).
"""
import RPi.GPIO as GPIO
import time

class RASPBERRY_PI_TRIGGER_BUTTON:

    def __init__(self):
        self.discard_pin = None
        self.pick_pin = None
        self.sort_pin = None

    def schedule(self, event_name, event_value,
                 discard_pin, pick_pin, sort_pin,
                 discard, pick, sort):

        if event_name == 'INIT':
            self.discard_pin = None
            self.pick_pin = None
            self.sort_pin = None
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.discard_pin, GPIO.OUT)
            GPIO.setup(self.pick_pin, GPIO.OUT)
            GPIO.setup(self.sort_pin, GPIO.OUT)
            GPIO.output(self.discard_pin, GPIO.HIGH)
            GPIO.output(self.pick_pin, GPIO.HIGH)
            GPIO.output(self.sort_pin, GPIO.HIGH)
            return [event_value, None]

        elif event_name == 'READ':
            if discard:
                GPIO.output(self.discard_pin, GPIO.LOW)
                GPIO.output(self.pick_pin, GPIO.HIGH)
                GPIO.output(self.sort_pin, GPIO.HIGH)
                time.sleep(1)
            elif

            return [None, event_value]
                    
                
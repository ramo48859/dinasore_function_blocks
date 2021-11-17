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
        self.pin_number = None
        self.result = None
        GPIO.setmode(GPIO.BOARD)

    def schedule(self, event_name, event_value,
                 pin_number):

        if event_name == 'INIT':
            self.pin_number = pin_number
            GPIO.setup(pin_number, GPIO.IN)
            return [event_value, None, True, True]

        elif event_name == 'READ':
            # Check button for 5 seconds
            timeout = time.time() + 5
            result = False
            while True:
                value = GPIO.input(pin_number)
                if bool(value) == True:
                    return [None, event_value, False, True]
                elif time.time() > timeout:
                    break
            return [None, event_value, True, False]
                    
                
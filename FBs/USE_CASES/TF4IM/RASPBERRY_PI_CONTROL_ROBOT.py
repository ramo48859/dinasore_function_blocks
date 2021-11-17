"""
This block takes a GPIO PIN Number (Board numbering scheme)
and if the button is pressed before timeout, FIRST_CONDITION is triggered.
SECOND condition is triggered if the button is not pressed befpre timeout.

ATENTION INVERSE LOGIC (because of the Arduino firmware used at the time).
"""
import RPi.GPIO as GPIO
import time

class RASPBERRY_PI_CONTROL_ROBOT:

    def __init__(self):
        self.discard_pin = None
        self.pick_pin = None
        self.sort_pin = None
        self.state = 0
        self.prevTime = 0

    def schedule(self, event_name, event_value,
                 discard_pin, pick_pin, sort_pin,
                 opcua_grab, button):

        if event_name == 'INIT':
            self.discard_pin = discard_pin
            self.pick_pin = pick_pin
            self.sort_pin = sort_pin
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.discard_pin, GPIO.OUT)
            GPIO.setup(self.pick_pin, GPIO.OUT)
            GPIO.setup(self.sort_pin, GPIO.OUT)
            GPIO.output(self.discard_pin, GPIO.HIGH)
            GPIO.output(self.pick_pin, GPIO.HIGH)
            GPIO.output(self.sort_pin, GPIO.HIGH)
            return [event_value, None]

        elif event_name == 'READ':
            
            currentTime = time.time()
            nextState = self.state
            
            #Read Inputs
            pick_in = opcua_grab
            discard_in = button

            #Calculate Next State
            if((self.state == 0) and (pick_in == True)):
                nextState = 1
            elif((self.state == 1) and (currentTime - self.prevTime > 1)):
                nextState = 2
            elif((self.state == 2) and (discard_in == True)):
                nextState = 3
            elif((self.state == 2) and (discard_in == False) and (currentTime - self.prevTime > 5)):
                nextState = 4
            elif((self.state == 3) and (currentTime - self.prevTime > 1)):
                nextState = 0
            elif((self.state == 4) and (currentTime - self.prevTime > 1)):
                nextState = 0
            
            #Actions in Transitions
            if((self.state == 0) and (nextState == 1)):
                self.prevTime = time.time()
            elif((self.state == 1) and (nextState == 2)):
                self.prevTime = time.time()
            elif((self.state == 2) and (nextState == 3)):
                self.prevTime = time.time()
            elif((self.state == 2) and (nextState == 4)):
                self.prevTime = time.time()
            
            #Update State
            self.state = nextState

            #Update Outputs
            if(self.state == 1):
                GPIO.output(self.discard_pin, GPIO.LOW)
            else:
                GPIO.output(self.discard_pin, GPIO.HIGH)

            if(self.state == 3):
                GPIO.output(self.pick_pin, GPIO.LOW)
            else:
                GPIO.output(self.discard_pin, GPIO.HIGH)
            
            if(self.state == 4):
                GPIO.output(self.sort_pin, GPIO.LOW)
            else:
                GPIO.output(self.discard_pin, GPIO.HIGH)
                

            return [None, event_value]
                    
                
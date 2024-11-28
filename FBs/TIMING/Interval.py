#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:26:57 2024

@author: david
"""

import pymodbus
try:
    from pymodbus.client import ModbusTcpClient
except:
    from pymodbus.client.sync import ModbusTcpClient #version workaround
    
    
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
import time
import numpy as np

import logging


class Interval:

    def __init__(self):
        self.client = None

    def schedule(self, event_name, event_value,interval):

        if event_name == 'INIT':
            self.interval = interval
            start = time.time()
            # caclculate first time an event is triggered
            # this is needed to ensure synchronous events 
            # across multiple instances
            
            #milliseconds since last complete second
            seconds = np.floor(start)
            fraction = start-seconds
            fullIntervals = fraction//interval
            if fraction % interval > 0.5:
                nexttime = (fullIntervals+2)*interval+seconds
            else:
                nexttime = (fullIntervals+1)*interval+seconds
            self.nexttime = nexttime
            
            print(f"nexttime:{nexttime}")
            return [None, event_value]

        elif event_name == 'READ':
            print("Read")
            
            delay = self.nexttime - time.time()
            if delay > 0:
                time.sleep(delay)
            self.nexttime = self.nexttime + self.interval
            logging.info("Triggering CLK event")
            
            return ["CLK", event_value]
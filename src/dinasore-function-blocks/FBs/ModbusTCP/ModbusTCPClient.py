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
import pandas as pd
from threading import Thread

import logging

log = logging.getLogger()


#Need for compatibility of old pymodbus running on pi and new pymodbus running on PC
if pymodbus.__version__.startswith("3"):
    def read_holding_registers_compat(client, myadr_dec, num, unitid):
        return client.read_holding_registers(myadr_dec, num, slave=unitid)
else:
    def read_holding_registers_compat(client, myadr_dec, num, unitid):
        return client.read_holding_registers(myadr_dec, num, unit=unitid)    


class ModbusTCPClient:

    def __init__(self):
        self.client = None

    def schedule(self, event_name, event_value,
                 hostname,port,uid):
        print(f"EventName:{event_name}")
        print(f"eventValue:{event_value}")
        print(f"hostname:{hostname}")
        print(f"port:{port}")
        print(f"uid: {uid}")
        if event_name == 'INIT':
            self.client = ModbusTcpClient(hostname,port)
            self.uid = uid
            return [event_value, None,(self.client,self.uid)]

        elif event_name == 'RUN':
            return [None, event_value,(self.client,self.uid)]
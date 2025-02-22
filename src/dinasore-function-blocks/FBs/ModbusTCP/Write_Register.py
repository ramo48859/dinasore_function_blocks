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



#-----------------------------------------
# Routine to read a float    
def writefloat(client,myadr_dec,unitid,val):
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_32bit_float(val)
    payload = builder.to_registers()
    response = client.write_registers(myadr_dec,payload,slave= unitid)
#write unsigned    
def writeUInt8(client,myadr_dec,unitid,val):
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_8bit_uint(val)
    payload = builder.to_registers()
    response = client.write_register(myadr_dec,*payload,slave= unitid)
def writeUInt16(client,myadr_dec,unitid,val):
    print(f"Writing {val} to modbus device")
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_16bit_uint(int(val))
    payload = builder.to_registers()
    print(f"payload:{payload}")
    response = client.write_register(myadr_dec,*payload,slave= unitid)
    print(f"response:{response}")
def writeUInt32(client,myadr_dec,unitid,val):
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_32bit_uint(val)
    payload = builder.to_registers()
    response = client.write_registers(myadr_dec,payload,slave= unitid)
def writeUInt64(client,myadr_dec,unitid,val):
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_64bit_uint(val)
    payload = builder.to_registers()
    response = client.write_registers(myadr_dec,payload,slave= unitid)   
#write signed
def writeSInt8(client,myadr_dec,unitid,val):
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_8bit_int(val)
    payload = builder.to_registers()
    response = client.write_register(myadr_dec,*payload,slave= unitid) 
def writeSInt16(client,myadr_dec,unitid,val):
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_16bit_int(val)
    payload = builder.to_registers()
    response = client.write_register(myadr_dec,*payload,slave= unitid)
def writeSInt32(client,myadr_dec,unitid,val):
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_32bit_int(val)
    payload = builder.to_registers()
    response = client.write_registers(myadr_dec,payload,slave= unitid)
def writeSInt64(client,myadr_dec,unitid,val):
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_64it_int(val)
    payload = builder.to_registers()
    response = client.write_registers(myadr_dec,payload,slave= unitid)


_writeOptions = {
    "UINT8" : writeUInt8,
    "UINT16" : writeUInt16,
    "UINT32": writeUInt32,
    "UINT64": writeUInt64,
    "SINT8": writeSInt8,
    "SINT8": writeSInt16,
    "SINT8": writeSInt32,
    "SINT8": writeSInt64,
    "FLOAT": writefloat
    }


class Write_Register:

    def __init__(self):
        self.client = None

    def schedule(self, event_name, event_value,client,address,type,value):
        
        print(f"EventName:{event_name}")
        print(f"eventValue:{event_value}")
        print(f"client:{client}")
        if event_name == 'INIT':
            self.address = address
            return [event_value, None,0.0]

        elif event_name == 'READ':
            self.uid = client[1]
            self.client = client[0]  
            self.address = address
            self.type = type
            
            print(f"value: {value}")
            
            #check if type is correct
            if type not in _writeOptions.keys():
                logging.error(f"Datatype provided for write is not one of {_writeOptions.keys()}!")
                raise ValueError
            
            try:
                val = _writeOptions[self.type](self.client,self.address,self.uid,value)
            except Exception as Argument:
                logging.error("""Could not write modbus registers. This chould be due to the following: \n
                             Client not reachable, incorrect unit id, address does not exist, register write access prohibited""",
                             stack_info=True, exc_info=True)
            return [None, event_value]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
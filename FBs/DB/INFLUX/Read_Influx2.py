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
def readfloat(client,myadr_dec,unitid):
    r1=read_holding_registers_compat(client,myadr_dec,2,unitid)
    FloatRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    result_FloatRegister =round(FloatRegister.decode_32bit_float(),2)
    return(result_FloatRegister)

#read unsigned
def readUInt8(client,myadr_dec,unitid):
    r1=read_holding_registers_compat(client,myadr_dec,1,unitid)
    IntRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    return IntRegister.decode_8bit_uint()
def readUInt16(client,myadr_dec,unitid):
    r1=read_holding_registers_compat(client,myadr_dec,1,unitid)
    IntRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    return IntRegister.decode_16bit_uint()
def readUInt32(client,myadr_dec,unitid):
    r1=read_holding_registers_compat(client,myadr_dec,2,unitid)
    IntRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    return IntRegister.decode_32bit_uint()
def readUInt64(client,myadr_dec,unitid):
    r1=read_holding_registers_compat(client,myadr_dec,4,unitid)
    IntRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    return IntRegister.decode_64bit_uint()
#read signed
def readSInt8(client,myadr_dec,unitid):
    r1=read_holding_registers_compat(client,myadr_dec,1,unitid)
    IntRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    return IntRegister.decode_8bit_int()
def readSInt16(client,myadr_dec,unitid):
    r1=read_holding_registers_compat(client,myadr_dec,1,unitid)
    IntRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    return IntRegister.decode_16bit_int()
def readSInt32(client,myadr_dec,unitid):
    r1=read_holding_registers_compat(client,myadr_dec,2,unitid)
    IntRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    return IntRegister.decode_32bit_int()
def readSInt64(client,myadr_dec,unitid):
    r1=read_holding_registers_compat(client,myadr_dec,4,unitid)
    IntRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    return IntRegister.decode_64bit_int()


_readOptions = {
    "UINT8" : readUInt8,
    "UINT16" : readUInt16,
    "UINT32": readUInt32,
    "UINT64": readUInt64,
    "SINT8": readSInt8,
    "SINT8": readSInt16,
    "SINT8": readSInt32,
    "SINT8": readSInt64,
    "FLOAT": readfloat
    }


class Read_Register:

    def __init__(self):
        self.client = None

    def schedule(self, event_name, event_value,client,address,type):
        
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
            
            print("Collect modbus measurement")
            #check if type is correct
            if type not in _readOptions.keys():
                log.error(f"Datatype provided for read is not one of {_readOptions.keys()}!")
                raise ValueError
            
            try:
                print(self.client)
                print(self.address)
                print(self.uid)
                val = _readOptions[self.type](self.client,self.address,self.uid)
                return [None, event_value,val]
            except:
                log.error("""Could not read modbus registers. This chould be due to the following: \n
                             Client not reachable, incorrect unit id, address does not exist, register read access prohibited""",
                             stack_info=True, exc_info=True)
            
            return [None, event_value,0]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:26:57 2024

@author: david
"""


import logging

from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from datetime import datetime,timezone



class Write_Influx2:

    def __init__(self):
        pass

    def schedule(self, event_name, event_value,
                 client,measurement, tag_name, tag_value,
                 field_name, value, timestamp):
        

        if event_name == 'INIT':
            logging.info("Init Event triggered")
            return [event_value]

        elif event_name == 'WRITE':
            #extract forecast reference times 
            logging.info("Write Event triggered")
            
            url = client[0]
            token = client[1]
            org = client[2]
            bucket = client[3]
            
                
            #construct datapoint
            p = Point(measurement)
            
            if (tag_name is not None) and (tag_value is not None):
                p = p.tag(tag_name, tag_value)
                
            p = p.field(field_name, value)
            
            if timestamp is not None:
                p = p.time(timestamp.astimezone(timezone.utc), WritePrecision.MS)
                
                
            logging.info(f"Writing point to db: {p}")
            
            #write to database
            with InfluxDBClient(url=url, token=token, org=org) as client:
                

                with client.write_api(write_options=SYNCHRONOUS) as write_api:
                    print(write_api.write(bucket=bucket, record=p,write_precision=WritePrecision.MS))
            return [None]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
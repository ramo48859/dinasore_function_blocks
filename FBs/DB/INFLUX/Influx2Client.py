#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:26:57 2024

@author: david
"""

    
    
from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import logging




class Influx2Client:

    def __init__(self):
        self.client = None

    def schedule(self, event_name, event_value,
                    url, token, org, bucket):
        if event_name == 'INIT':
            self.url = url
            self.token = token
            self.org = org
            self.bucket = bucket
            logging.info("Init influx client")
            return [event_value,(self.url,
                                 self.token,
                                 self.org,
                                 self.bucket)]

        elif event_name == 'RUN':
            return [None,(self.url,
                          self.token,
                          self.org,
                          self.bucket)]
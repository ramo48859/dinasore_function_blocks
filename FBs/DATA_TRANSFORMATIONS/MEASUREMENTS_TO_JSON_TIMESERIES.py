import json
import pandas as pd
import numpy as np

""" 
This block takes a list of measurments, the initial timestamp, and the sampling frequency 
and converts these to a JSON formated timeseries

This block was created to insert data in a table with the following column structure:
sensor_id|timestamp|measuremnt

Pandas frequency step units
H 	Hours
T 	Minutes 		
S 	Seconds 		
L 	Milliseonds 		
U 	Microseconds 		
N 	nanoseconds  

The initial timestamp must be in ISO format e.g. 2015-07-03T10:32:01.020000Z
The measurements list must be a ';' separated list of floats

To run this block in a Raspberry Pi 3 you may need to install the following dependencies:
sudo apt-get install python-dev libatlas-base-dev
"""	

class MEASUREMENTS_TO_JSON_TIMESERIES:

    def __init__(self):
        self.sensor_id = None
        self.frequency_step_units = None
        
    def schedule(self, event_name, event_value,
                 SENSOR_ID, MEASUREMENTS, INITIAL_TIMESTAMP, FREQUENCY_STEP_UNITS):

        if event_name == 'INIT':
            self.sensor_id = int(SENSOR_ID)
            self.frequency_step_units = FREQUENCY_STEP_UNITS

            return [event_value, 
                self.sensor_id,
                None,
                None,
                self.frequency_step_units,
                None]


        elif event_name == 'RUN':
            string_list = np.array(MEASUREMENTS.split(";"))
            floats_list = string_list.astype(float)
            sensor_measurements = [(self.sensor_id,MEASUREMENTS[x]) for x in range(len(floats_list))]
            timeseries = pd.DataFrame(sensor_measurements, columns=["measurement","sensor"], index=pd.date_range(INITIAL_TIMESTAMP, periods=len(floats_list), freq="L"))
            result = timeseries.to_json(orient="split", date_format="iso", date_unit="us")
            print(result)
            return [event_value, 
                self.sensor_id ,
                MEASUREMENTS,
                INITIAL_TIMESTAMP,
                self.frequency_step_units,
                result]

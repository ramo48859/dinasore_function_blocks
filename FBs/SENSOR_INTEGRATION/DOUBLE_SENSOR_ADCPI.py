import time
import pandas as pd
from multiprocessing import Process, Manager
from ADCPi import ADCPi

"""
This block is used with an ADCPI hat, on a Raspberry Pi, to collect data  in parallel, from two sensors.
Each sensor will have its own list of measurements and the list of timestamps is shared.

https://www.abelectronics.co.uk/p/69/adc-pi-raspberry-pi-analogue-to-digital-converter

Check the link below to instal the required ADCPi libraries
https://github.com/abelectronicsuk/ABElectronics_Python_Libraries
"""

def read_from_adc(pin_number, adc_object, meas_list, tstamps_list, samples):
    for i in range(samples):
        meas_list[i] = adc_object.read_raw(pin_number)
        if tstamps_list != None:
            tstamps_list[i] = pd.Timestamp.now()
    for i in range(samples):
        voltage = float(0.0)
        voltage = float((meas_list[i] * (adc_object.__lsb / adc_object.__pga)) * 2.471)
        meas_list[i] = voltage

class DOUBLE_SENSOR_ADCPI:

    def __init__(self):
        self.first_adc = None
        self.second_adc = None
        self.first_measurements_list = None
        self.second_measurements_list = None
        self.first_pin = 1
        self.second_pin = 1
        self.first_process = None
        self.second_process = None
        self.timestamps_list = None
        self.samples = 1
        self.manager = None

    def create_meas_series(self, meas_list):
        i = 0
        value = ""
        while i < self.samples-1:
            value = value + str(meas_list[i]) + ";"
            i += 1
        value = value + str(meas_list[self.samples-1])
        return value
    
    def create_tstamp_series(self, tstamps_list):
        i = 0
        times = ""
        while i < self.samples-1:
            times = times + str(tstamps_list[i]) + ";"
            i += 1
        times = times + str(tstamps_list[self.samples-1]) 
        return times

    def schedule(self, event_name, event_value, 
    FIRST_PIN, SECOND_PIN, SAMPLES):
        
        ### INIT EVENT ###
        if event_name == 'INIT':
    
            if SIZE is None or SIZE < 1:
                return [None, None, None, None, None]
            if PIN is None or PIN < 1:
                return [None, None, None, None, None]
    
            self.first_adc = ADCPi(0x68, 0x69, 12)
            self.second_adc = ADCPi(0x68, 0x69, 12)
            self.samples = SIZE
            self.first_pin = FIRST_PIN
            self.second_pin = SECOND_PIN
            self.manager = Manager()
            self.first_measurements_list = manager.list(range(SIZE))
            self.second_measurements_list = manager.list(range(SIZE))
            self.timestamps_list = manager.list(range(SIZE))

            #Create the first sensor process
            self.first_process = Process(
                target=read_from_adc, 
                args=(self.first_pin, 
                    self.first_adc, 
                    self.first_measurements_list,
                    self.timestamps_list,
                    self.samples)
            )
            #Create the second sensor process
            self.second_process = Process(
                target=read_from_adc, 
                args=(self.second_pin, 
                    self.second_adc, 
                    self.second_measurements_list,
                    None,
                    self.samples)
            )
            
            print("ADCPi init")

            return [event_value, None, None, None, None]
        
        ### READ EVENT ###
        elif event_name == 'READ':
            
            print("ADCPi read")
            
            self.first_process.start()
            self.second_process.start()
            self.first_process.join()
            self.second_pocess.join()

            print("ADCPi read done")

            result_1 = create_meas_series(self.first_measurements_list)
            result_2 = create_meas_series(self.second_measurements_list)
            times = create_tstamp_series(self.timestamps_list)
            
            print("Result_1")
            print(result_1)
            
            print("Result_2")
            print(result_12)
            
            print("Times")
            print(times)

            return [None, event_value, result_1, result_2, times]
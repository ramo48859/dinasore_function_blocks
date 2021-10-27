import time
from ADCPi import ADCPi

class SENSOR_ADCPI:

    def __init__(self):
        self.adc = None
        self.measurements_list=[]
        self.size = 1
        self.pin = 1

    def schedule(self, event_name, event_value, T_CYCLE, PIN, SIZE):

        if event_name == 'INIT':
            self.adc = ADCPi(0x68, 0x69, 18)
            if SIZE is None or SIZE < 1:
                return [None, None, None, None]
            if PIN is None or PIN < 1:
                return [None, None, None, None]
            self.size = SIZE
            self.pin = PIN
            print("ADCPi init")
            return [None, event_value, None, None, None]

        elif event_name == 'READ':
            print("ADCPi read")
            i = 0
            value = 0
            while i < self.size:
                value = self.adc.read_voltage(self.pin)
                self.measurements_list.append(value)
                print(value)
                time.sleep(0.1)
                i+=1

            value = [str(x) for x in self.measurements_list]
            print(value)
            self.measurements_list = []
            return [None, event_value, value]


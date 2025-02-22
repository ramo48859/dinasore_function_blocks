
from ipaddress import ip_address
import snap7
from snap7 import types
from datetime import datetime, timedelta
import time
class S7_READ_CONTINUOUS_PRESS:    
    def __init__(self):
        self.state = None
        self.client = snap7.client.Client()
        self.bits = [0,0,0,0,0,0,0,0]
        self.old_value = 0
        self.first_time = True
        self.counter = None
        self.right_state_previous = 0
        self.output_previous = 0
        self.time_in = 0
        self.time_out = 0

    def schedule(self, event_name, event_value, ip_address, rack, number, port, station_id, part_id):
        
        if event_name == 'INIT':
            try:
                self.client.connect(ip_address,rack,number,port)
                status = self.client.get_connected()
            except:
                status = False

            self.station_id = station_id
            if(status == True):
                print('Connection sucessfully initiated with device at {0}'.format(ip_address))
            else:
                print('Error initiating connection with S7 PLC')
            self.state = 0
            
            return [event_value, None, None, None]

        elif event_name == 'READ':            
            
            #input = self.client.read_area(types.Areas.PA,0,8,1)
            #input_value = int.from_bytes(input,"big")
            try:
                output = self.client.read_area(types.Areas.PA,0,8,1)
            except:
                return [None, event_value, None,None]
            output_value = int.from_bytes(output,"big")

            #0x15 -> Any of the green lights is on
            if(self.state == 0 and output_value & 0x15 != 0):
                self.state=1
                self.time_in = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S.%f')
                #print(self.state, hex(output_value))


            elif(self.state == 1 and ((self.output_previous & 0xc0)!=0 and (output_value & 0xb0) == 0) ):
                self.state =0
                time_out = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S.%f')
                if(output_value & 0x40):
                    database_string = str(station_id)  + ',' + str(part_id) + ',\'' +self.time_in+ '\',\'' +  time_out + '\',True'

                else:
                    database_string = str(station_id)  + ',' + str(part_id) + ',\'' +self.time_in+ '\',\'' +  time_out + '\',False'
                
                return [None, event_value,event_value,database_string]
            

            self.output_previous = output_value
            
            return [None, event_value, None,None] 
            


    

    def __del__(self):
        self.client.__del__()

from ipaddress import ip_address
import snap7
from datetime import datetime, timedelta
import time
class S7_READ_CONTINUOUS_SOLDERING:    
    def __init__(self):
        self.state = None
        self.client = snap7.client.Client()
        self.bits = [0,0,0,0,0,0,0,0]
        self.old_value = 0
        self.first_time = True
        self.counter = None
        self.right_state_previous = 0
        self.left_state_previous = 0

    def schedule(self, event_name, event_value, ip_address, rack, number, port, station_id, part_id, left_block, right_block):
        
        if event_name == 'INIT':
            try:
                self.client.connect(ip_address,rack,number,port)
                status = self.client.get_connected()
            except:
                status = False
            if(status == True):
                print('Connection sucessfully initiated with device at {0}'.format(ip_address))
            else:
                print('Error initiating connection with S7 PLC')
            return [event_value, None, None, None]

        elif event_name == 'READ':            
            try:
                counter = self.client.db_read(16,0,4)
            except:
                self.client.connect(ip_address,rack,number,port)

                return [None, event_value, None,None] 
            counter_value =  int.from_bytes(counter, "big")
            right_state = int.from_bytes(self.client.db_read(8,right_block,2),"big")
            time_in = ""
            time_out = ""
            if part_id == -1:
                part_id = int(time.time() )


            if(right_state - self.right_state_previous > 0 ):
                time_right_per_piece = int.from_bytes(self.client.db_read(34,20,4),"big")
                time_in = datetime.strftime(datetime.now() - timedelta(microseconds=time_right_per_piece*1000),'%Y-%m-%d %H:%M:%S.%f')
                time_out = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S.%f')
                if(right_state == 1):
                    database_string = str(station_id)  + ',' + str(part_id) + ',\'' +time_in+ '\',\'' +  time_out + '\',True'
                else:
                    database_string =  str(station_id)  + ',' + str(part_id) + ',\'' +time_in+ '\',\'' +  time_out + '\',False'
                self.right_state_previous = right_state
                #print(database_string)
                return [None, event_value, event_value, database_string]

            left_state = int.from_bytes(self.client.db_read(8,left_block,2),"big")

            if(left_state - self.left_state_previous > 0 ):
                time_left_per_piece = int.from_bytes(self.client.db_read(34,8,4),"big")
                time_in = datetime.strftime(datetime.now() - timedelta(microseconds=time_left_per_piece*1000),'%Y-%m-%d %H:%M:%S.%f')
                time_out = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S.%f')
                if(left_state == 1):
                    database_string = str(station_id)  + ',' + str(part_id) + ',\'' +time_in+ '\',\'' +  time_out + '\',True'
                else:
                    database_string =  str(station_id)  + ',' + str(part_id) + ',\'' +time_in+ '\',\'' +  time_out + '\',False'

                self.left_state_previous =left_state

                #print(database_string)
                return [None, event_value, event_value, database_string]
            self.right_state_previous = right_state
            self.left_state_previous =left_state
            return [None, event_value, None,None] 
            


    

    def __del__(self):
        self.client.__del__()
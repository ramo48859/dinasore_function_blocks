
from datetime import datetime
import time

class STATION_MANAGER:    
    def __init__(self):
        self.station_id = 0
        pass

    def schedule(self, event_name, event_value, START_STATION_BIT,STATION_ID, PART_ID, END_STATION_OK_BIT,END_STATION_NOK_BIT):

        #initialization of ouptut events
        INIT_O_EVENT = None
        RUN_O_EVENT = None
        SET_STATION_OUT_EVENT = None
        DATABASE_INSERTION_EVENT = None
        START_NEXT_STATION_EVENT = None
        

        #initialization of output variables
        part_id = 0
        start_next_station_bit = 0
        station_out_bit = 0
        database_string = ""

        print(event_name, event_value)
        if event_name == 'INIT':
            self.parts_queue =  []
            self.station_id = STATION_ID
            INIT_O_EVENT = 1
        elif event_name == 'RUN':  
            RUN_O_EVENT  = 1
            pass

        elif event_name == 'START_STATION' and START_STATION_BIT:
            self.station_1_out_bit = 1 
            if PART_ID == -1:
                part_id = int(time.time())
            else:
                part_id = PART_ID
            self.parts_queue.append({'part_id': part_id, 'time_in': datetime.now(), 'time_out':0})
            SET_STATION_OUT_EVENT = 1
            station_out_bit = True
            
        elif event_name == 'END_STATION_OK' and END_STATION_OK_BIT:

            part = self.parts_queue.pop(0)
            part['time_out'] = datetime.now()
            station_out_bit = 0 
            DATABASE_INSERTION_EVENT = 1
            if len(self.parts_queue) == 0:
                SET_STATION_OUT_EVENT = 1
                station_out_bit = False
            START_NEXT_STATION_EVENT = 1
            start_next_station_bit =1
            DATABASE_INSERTION_EVENT = 1
            part_id = part['part_id']
            database_string = str(self.station_id)  + ',' + str(part['part_id']) + ',\'' + datetime.strftime(part['time_in'],'%Y-%m-%d %H:%M:%S.%f') + '\',\'' + datetime.strftime(part['time_out'],'%Y-%m-%dT%H:%M:%S.%f') + '\',True'
            print(database_string)
            print(part)
            
        elif event_name == 'END_STATION_NOK' and END_STATION_NOK_BIT:
            part = self.parts_queue.pop(0)
            part['time_out'] = datetime.now()
            station_out_bit = 0 
            DATABASE_INSERTION_EVENT = 1
            if len(self.parts_queue) == 0:
                SET_STATION_OUT_EVENT = 1
                station_out_bit = False
            station_out_bit = 0 
            DATABASE_INSERTION_EVENT = 1 
            database_string = str(self.station_id) + ',' + str(part['part_id']) +  ',\'' + datetime.strftime(part['time_in'],'%Y-%m-%d %H:%M:%S.%f') + '\',\'' + datetime.strftime(part['time_out'],'%Y-%m-%dT%H:%M:%S.%f') + '\',False'

            print(part)

        print(self.parts_queue)
            

        return [INIT_O_EVENT, RUN_O_EVENT , START_NEXT_STATION_EVENT, SET_STATION_OUT_EVENT, DATABASE_INSERTION_EVENT,  part_id, start_next_station_bit, station_out_bit, database_string]


        
    
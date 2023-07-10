
from datetime import datetime
import time

class SCREW_STATION_MANAGER:    
    def __init__(self):
        self.station_id = 0
        self.ok = 0
        self.nok = 0
        self.part = None
        pass

    def schedule(self, event_name, event_value, START_STATION_BIT,STATION_ID, PART_ID, NUMBER_OF_SCREWS, SIGNAL_SCREW_OK_BIT,SIGNAL_SCREW_NOK_BIT, END_STATION_BIT):

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
            self.station_id = STATION_ID
            INIT_O_EVENT = 1
        elif event_name == 'RUN':  
            RUN_O_EVENT  = 1
            pass

        elif event_name == 'START_STATION' and START_STATION_BIT:
            self.number_of_screws = NUMBER_OF_SCREWS
            if PART_ID == -1:
                part_id = int(time.time())
            else:
                part_id = PART_ID
            self.part  =   {'part_id': part_id, 'time_in': datetime.now(), 'time_out':0}

            self.ok = 0
            self.nok = 0


            
        elif event_name == 'SIGNAL_SCREW_OK' and SIGNAL_SCREW_OK_BIT:

            self.ok = self.ok +1
            #print(database_string)
            #print(self.part)
            
        elif event_name == 'SIGNAL_SCREW_NOK' and SIGNAL_SCREW_NOK_BIT:
            self.nok = self.nok +1

            #database_string = str(self.station_id) + ',' + str(part['part_id']) +  ',\'' + datetime.strftime(part['time_in'],'%Y-%m-%d %H:%M:%S.%f') + '\',\'' + datetime.strftime(part['time_out'],'%Y-%m-%dT%H:%M:%S.%f') + '\',False'

            print(part)

        elif event_name == 'END_STATION':
            #print('here')
            #print(self.part)
            if(self.part != None):
                self.part['time_out'] = datetime.now()
                #print(self.ok)
                #print(self.number_of_screws)
                if(self.ok >= self.number_of_screws):
                    database_string = str(self.station_id)  + ',' + str(self.part['part_id']) + ',\'' + datetime.strftime(self.part['time_in'],'%Y-%m-%d %H:%M:%S.%f') + '\',\'' + datetime.strftime(self.part['time_out'],'%Y-%m-%dT%H:%M:%S.%f') + '\',True'
                else:
                    database_string = str(self.station_id)  + ',' + str(self.part['part_id']) + ',\'' + datetime.strftime(self.part['time_in'],'%Y-%m-%d %H:%M:%S.%f') + '\',\'' + datetime.strftime(self.part['time_out'],'%Y-%m-%dT%H:%M:%S.%f') + '\',False'

                DATABASE_INSERTION_EVENT = 1 

            #print(database_string)
        return [INIT_O_EVENT, RUN_O_EVENT , START_NEXT_STATION_EVENT, SET_STATION_OUT_EVENT, DATABASE_INSERTION_EVENT,  part_id, start_next_station_bit, station_out_bit, database_string]


        
    
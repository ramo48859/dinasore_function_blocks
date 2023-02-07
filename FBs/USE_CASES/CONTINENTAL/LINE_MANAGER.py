
import time

class LINE_MANAGER:    
    def __init__(self):
        self.data = 0
        self.beggining_state= 0
        self.station
        self.station_1_out_bit = 0
        self.station_2_out_bit = 0
        self.station_3_out_bit = 0
        pass

    def schedule(self, event_name, event_value, START_STATION_1_BIT,END_STATION_1_OK_BIT,END_STATION_1_NOK_BIT,END_STATION_2_OK_BIT,END_STATION_2_NOK_BIT,END_STATION_3_OK_BIT,END_STATION_3_NOK_BIT):
        
        print(event_name, event_value)
        if event_name == 'INIT':
            self.parts_state =  {}
            self.nextId = 1
            self.beggining_state = 1
        elif event_name == 'RUN':  
            pass

        elif event_name == 'START_STATION_1' and START_STATION_1_BIT:
            self.station_1_out_bit = 1 
            

        elif event_name == 'END_STATION_1_OK':
            self.station_1_out_bit = 0 
            self.station_2_out_bit = 1
  

        elif event_name == 'END_STATION_1_NOK':
            self.station_1_out_bit = 0   

        elif event_name == 'END_STATION_2_OK'
            self.station_2_out_bit = 0
            pass  

        elif event_name == 'END_STATION_2_NOK':
            pass  

        elif event_name == 'END_STATION_3_OK':
            pass            
        
        elif event_name == 'END_STATION_3_NOK': 
            pass

        return [None,None,  1, None, None, None,None, self.data, self.beggining_state, self.station_1_out_bit, self.station_2_out_bit, self.station_3_out_bit, database_string]


        
    
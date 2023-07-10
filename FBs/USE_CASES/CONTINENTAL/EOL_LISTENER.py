from ipaddress import ip_address
from datetime import datetime, timedelta
import time
import socket
class EOL_LISTENER:    
    def __init__(self):
        self.socket = None
        self.in_timestamp = None

    def schedule(self, event_name, event_value, ip_address,port, station_id, part_id):
        
        if event_name == 'INIT':
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((ip_address,port))
            self.socket.listen()
            return [event_value, None, None, None]

        elif event_name == 'READ':            
            conn, addr = self.socket.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    print(data)
                    data_split = data.split(";")
                    if len(data)>1 :
                        self.in_timestamp = data_split[1]
                        return [None, event_value, None, None]
                    else:
                        result = data_split[1]
                        out_time_stamp = data_split[2]
                        database_string = station_id  + ',' + part_id + ',\'' +  self.in_timestamp  + '\',\'' + out_time_stamp + '\',' + result
                        return [None, event_value,True, database_string]

            return [None, event_value, None,None] 
            


    

    def __del__(self):
        self.client.__del__()
from ipaddress import ip_address
from datetime import datetime, timedelta
import time
import socket
class EOL_LISTENER:    
    def __init__(self):
        self.socket = None
        self.in_timestamp = None
        self.socket_is_alive = False

        

    def schedule(self, event_name, event_value, ip_address,port, station_id, part_id):
        
        if event_name == 'INIT':
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((ip_address,port))
            self.socket.listen()
            self.socket_is_alive = True
            print("Socket Opened")
            return [event_value, None, None, None]

        elif event_name == 'READ':            
            conn, addr = self.socket.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    print("DATA:", flush=True)
                    print(data)
                    data_split = data.decode('utf-8').split(";")
                    print(data_split,len(data))
                    if len(data_split)==1 :
                        self.in_timestamp = data_split[0]
                        return [None, event_value, None, None]
                    else:
                        result = True if  data_split[0]=="OK" else False
                        out_time_stamp = data_split[1]
                        
                        database_string = str(station_id)  + ',' + str(part_id) + ',\'' +  str(self.in_timestamp)  + '\',\'' + str(out_time_stamp) + '\',' + str(result)
                        return [None, event_value,True, database_string]

            return [None, event_value, None,None] 
            


    

    def __del__(self):
        if(self.socket != None and self.socket_is_alive):
            self.socket.close()
            self.socket_is_alive = False
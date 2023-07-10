from ipaddress import ip_address
from datetime import datetime, timedelta
import time
import socket
class EOL_LISTENER:    
    def __init__(self):
        self.socket = None

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
                    return [None, event_value,True, data]

            return [None, event_value, None,None] 
            


    

    def __del__(self):
        self.client.__del__()
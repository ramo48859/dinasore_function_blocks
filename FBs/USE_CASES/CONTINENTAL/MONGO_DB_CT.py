from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv
import json
import statistics
from getmac import get_mac_address
import socket

def collect_cycle_times(table, x):
    cycle_times = []
    results = table.find().sort('_id', -1).limit(x)
    for result in results:
        cycle_times.append(result['value'])
    return cycle_times

class MONGO_DB_CT:
    def schedule(self, event_input_name, event_input_value, host, port, past_x, SerialNumbers, m_criticals):
        criticals = [None]*8
        if event_input_name == 'INIT':
            load_dotenv()
            user = environ.get('MONGO_USER')
            password = environ.get('PASSWORD')
            self.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.database = self.client['diginental']

            return [event_input_value, None, None]+criticals

        elif event_input_name == 'RUN':
            if m_criticals != "" and m_criticals != None:
                criticals_dict = json.loads(m_criticals)
                for key, value in criticals_dict.items():
                    index = int(key.split("_")[1])
                    criticals[index-1] = value
                
            if SerialNumbers == "":
                return [None, event_input_value, None]+criticals

            if SerialNumbers is None:
                return [None, None, None]+criticals
            
            serials = json.loads(SerialNumbers)
            data = {}
            for serial in serials:
                cons = collect_cycle_times(self.database["time_"+str(serial)], past_x)
                mean = round(statistics.mean(cons), 2)
                st_dev = round(statistics.stdev(cons), 2)
                data["time_"+str(serial)+"_avg"] = mean
                data["time_"+str(serial)+"_std"] = st_dev
            data = json.dumps(data)
            #print(data, criticals)
            return [None, event_input_value, data]+criticals

#a = MONGO_DB_CT()
#b=a.schedule("INIT", 1, "localhost", 27017, 5, "[1, 2, 3, 4, 5, 6, 7, 8]", None)
#b=a.schedule("RUN", 1, "localhost", 27017, 5, "[1, 2, 3, 4, 5, 6, 7, 8]", None)
#print(b)
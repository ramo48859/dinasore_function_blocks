from pymongo import MongoClient
from os import environ
from getmac import get_mac_address
import socket
from dotenv import load_dotenv
from datetime import datetime

class CYCLE_DONE:
    def schedule(self, event_input_name, event_input_value, host, port, line, start_str, end_str):
        if event_input_name == 'INIT':
            # Connect to db
            load_dotenv()
            user = environ.get('MONGO_USER')
            password = environ.get('PASSWORD')
            client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.db = client.diginental
            return [event_input_value, None]

        elif event_input_name == 'RUN':
            if end_str == "":
                self.cached = start_str
                return [event_input_value, None]

            # Calculate cycle time and insert in db
            start_values = self.cached.split(',') if start_str == "" else start_str.split(',')
            end_values = end_str.split(',')
            timestamp_start = datetime.strptime(start_values[2].replace('\'', '').split('.')[0], "%Y-%m-%d %H:%M:%S").timestamp()
            timestamp_finish = datetime.strptime(end_values[3].replace('\'', '').split('.')[0], "%Y-%m-%dT%H:%M:%S").timestamp()
            self.db['time_' + line].insert_one({
                'timestamp': timestamp_finish,
                'value': timestamp_finish - timestamp_start
            })
            print("Wrote the cycle time in the database. - " + str(timestamp_finish - timestamp_start))

            # Increment pieces done
            aux = list(self.db.lines.find({'name': line}))[0]['piecesDone']
            self.db.lines.update_one(
                {'name': line},
                {'$set': {'piecesDone': aux + 1}}
            )

            return [event_input_value, None]
from datetime import datetime
import json
from pymongo import MongoClient
from os import environ
import json
from dotenv import load_dotenv

class MONGO_WRAPPER:
    def schedule(self, event_input_name, event_input_value, values, host, port):
        if event_input_name == 'INIT':
            # Connect to db
            load_dotenv()
            user = environ.get('MONGO_USER')
            password = environ.get('PASSWORD')
            client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.db = client.diginental
            return [event_input_value, None, []]

        elif event_input_name == 'RUN':
            values = values.split(',')
            timestamp_start = datetime.strptime(values[2].replace('\'', '').split('.')[0], "%Y-%m-%d %H:%M:%S").timestamp()
            timestamp_finish = datetime.strptime(values[3].replace('\'', '').split('.')[0], "%Y-%m-%dT%H:%M:%S").timestamp()
            value = {'serialNumber': values[0], 'type': "time", 'value': timestamp_finish - timestamp_start}

            # Increment machine counter
            aux = list(self.db.machines.find({'serialNumber': str(values[0])}))[0]['piecesUntilMaintenance']
            self.db.machines.update_one(
                {'serialNumber': str(values[0])},
                {'$set': {'piecesUntilMaintenance': aux - 1}}
            )
            print("Piece done at machine - " + str(values[0]))

            if values[4] == 'False':
                # Increment machine counter
                aux = list(self.db.machines.find({'serialNumber': str(values[0])}))[0]['defects']
                self.db.machines.update_one(
                    {'serialNumber': str(values[0])},
                    {'$set': {'defects': aux + 1}}
                )

                # Increment line counter
                line = list(self.db.machines.find({'serialNumber': str(values[0])}))[0]['line']
                aux = list(self.db.lines.find({'name': line}))[0]['defects']
                self.db.lines.update_one(
                    {'name': line},
                    {'$set': {'defects': aux + 1}}
                )

            return [None, event_input_value, str(value).replace("\'", "\"")]

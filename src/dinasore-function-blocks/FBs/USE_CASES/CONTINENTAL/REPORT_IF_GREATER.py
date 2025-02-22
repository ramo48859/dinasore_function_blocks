import sys
from pymongo import MongoClient
from os import environ
from getmac import get_mac_address
import socket
import json
from dotenv import load_dotenv

def findAllWithProperty(collection, property):
    data = []
    cursor = collection.find(property)

    for element in cursor:
        data.append(element)

    return data

def createProperty(arguments):
    if len(arguments) % 2 != 0:
        return {}
    data = {}
    for i in range(0, len(arguments), 2):
        data[arguments[i]] = arguments[i + 1]
    return data

def stopMachine(collection, SN):
    filter = {"serialNumber": SN}
    update = {"$set": {"state": "stopped"}}
    collection.update_one(filter, update)

def insertInCollection(collection, data):
    collection.insert_one(data)

def checkMachine(collection, sn):
    prop = createProperty(['serialNumber', str(sn)])
    data = findAllWithProperty(collection, prop)
    return len(data) > 0

class REPORT_IF_GREATER:

    def schedule(self, event_input_name, event_input_value, value, limit, critical, type, reportMessage, host, port, serialNumber):
        if event_input_name == 'INIT':
            # Connect to db
            load_dotenv()
            user = environ.get('MONGO_USER')
            password = environ.get('PASSWORD')
            client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.db = client.diginental
            perm = self.db['machines']
            notif = self.db['notifications']

            if checkMachine(perm, serialNumber):
                self.valid = True
                print('Registered Machine!\nWelcome!')
            else:
                self.valid = False
                insertInCollection(notif, createProperty(['serialNumber', serialNumber, 'roleLevel', 3,
                                                          'message',
                                                          f'Machine "{serialNumber}" tried to connect but no machine found in database\nWant to add it?',
                                                          'read', False]))
                print('Machine not in the database!\nRequested to create the machine in the database. (please reopen de dinasore)')

            return [event_input_value, None, None, None]

        elif event_input_name == 'RUN':
            if not self.valid: return [event_input_value, None, None, None]
            
            tmp = json.loads(value)
            self.report = {'serialNumber': serialNumber, 'type': type, 'text': reportMessage}

            if tmp['value'] > critical:
                print('Value above critical!')

                perm = self.db['machines']
                notif = self.db['notifications']
                stopMachine(perm, serialNumber)
                insertInCollection(notif, createProperty(['serialNumber', serialNumber, 'roleLevel', 1,
                                                              'message', f'The sensor "{tmp["type"]}" from machine "{serialNumber}" got above the critical value: {critical}. Dinasore Terminated.',
                                                              'read', False]))
            if tmp['value'] > limit:
                return [None, event_input_value, value, str(self.report).replace("\'", "\"")]

            return [None, event_input_value, value, None]
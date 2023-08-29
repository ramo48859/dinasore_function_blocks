from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv
from datetime import datetime
from getmac import get_mac_address
import socket
import json

def insertManyInCollection(collection, data):
    collection.insert_many(data)

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

class MONGO_DB_INSERT:
    def schedule(self, event_input_name, event_input_value, data, host, port):
        if event_input_name == 'INIT':
            load_dotenv()
            user = environ.get('MONGO_USER')
            password = environ.get('PASSWORD')
            self.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.database = self.client['diginental']

            return [event_input_value, None, []]

        elif event_input_name == 'RUN':

            if data == "":
                return [None, event_input_value, "OK"]

            if data is None:
                return [None, None, None]

            dictData = json.loads(data)
            toDB = {}

            for key in dictData:

                if "text" in dictData[key]:
                    collName = f"logs_{dictData[key]['serialNumber']}"
                    if "collName" not in toDB:
                        toDB[collName] = []
                    toDB[collName].append(dictData[key])

                else:
                    collName = f"{dictData[key]['type']}_{dictData[key]['serialNumber']}"

                    if collName not in toDB:
                        toDB[collName] = []
                    d = {k: dictData[key][k] for k in dictData[key] if k not in ['type']}
                    toDB[collName].append(d)

            for key in toDB:
                collName = key
                collection = self.database[collName]
                insertManyInCollection(collection, toDB[key])
                print(f"Wrote: {len(toDB[key])} values to the collection: {collName}")

            return [None, event_input_value, "OK"]
from datetime import datetime
import json

def createProperty(arguments):
    if len(arguments) % 2 != 0:
        return {}
    data = {}
    for i in range(0, len(arguments), 2):
        data[arguments[i]] = arguments[i + 1]
    return data

class VALUES_TO_JSON:

    def schedule(self, event_input_name, event_input_value, value1, value2, value3, value4, value5, value6, value7,
                 value8, value9, value10, time):

        if event_input_name == 'INIT':
            self.time = time
            self.time = ""
            self.ready = False
            self.data = {}

            return [event_input_value, None, []]

        elif event_input_name == 'RUN':

            dateTime = datetime.now()

            timeStamp = datetime.timestamp(dateTime)
            values = [value1, value2, value3, value4, value5, value6, value7, value8, value9, value10]

            size = len(self.data)


            if size != 0:
                firstTime = self.data['0']['timestamp']
                if timeStamp - firstTime >= time:
                    ret = str(self.data).replace("\'", "\"")
                    self.data = {}
                    return [None, event_input_value, ret]

            for value in values:
                if value is None:
                    continue
                tmp = json.loads(value)
                if "value" in tmp:
                    prop = createProperty(['serialNumber', tmp["serialNumber"], 'type', tmp["type"], 'value', tmp["value"], 'timestamp',
                                           timeStamp])
                else:
                    prop = createProperty(
                        ['serialNumber', tmp["serialNumber"], 'type', tmp["type"], 'text', tmp["text"], 'timestamp',
                         timeStamp])
                self.data[f'{size}'] = prop
                size += 1

            return [None, event_input_value, ""]

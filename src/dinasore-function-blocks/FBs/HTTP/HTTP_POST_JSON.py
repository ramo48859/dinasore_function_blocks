# pip install requests

import requests
import json

class HTTP_POST_JSON:

    def schedule(self, event_input_name, event_input_value, 
        url, timeout, json_content):

        if event_input_name == 'INIT':
            return [None, event_input_value, None]
        elif event_input_name == 'RUN':
            #json_obj = json.loads(json_content)
            req = requests.post(url, json=json_content, timeout=timeout)
            return [None, event_input_value, req.status_code]
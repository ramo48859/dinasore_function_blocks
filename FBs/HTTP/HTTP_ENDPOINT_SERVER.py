# pip install flask

from flask import Flask, request, jsonify, abort, Response
from multiprocessing import Queue
import threading

"""
Because of the way FB's are implemented, the HTTP server and REST processing have to be detached 
from the FB execution.
This StackOverflow post provided the answer to do that using Flask:
https://stackoverflow.com/questions/60490621/passing-an-external-queue-to-flask-route-function
Code adapted from StackOverflow post.
"""
class ControllableServer(threading.Thread):

    class _URLCallbackClass():
        def __init__(self, output_queue):
            self.output_queue = output_queue

        def url_callback(self):
            content = request.json
            if content is None:
                abort(404, description="Content not found.")
            self.output_queue.put(content)
            return Response(content, 200)

    def __init__(self, output_queue, host, port, endpoint):
        super().__init__(daemon=True)
        self.output_queue = output_queue
        self.host = host
        self.port = port
        self.endpoint = endpoint
        self._flask = Flask(__name__)

    def run(self):
        callback_class = ControllableServer._URLCallbackClass(self.output_queue)
        #self._flask.add_url_rule('/edge', 'url_callback', callback_class.url_callback, methods=["POST","PUT"])
        self._flask.add_url_rule(self.endpoint, 'url_callback', callback_class.url_callback, methods=["POST","PUT"])
        self._flask.run(self.host, self.port)                           

class HTTP_ENDPOINT_SERVER:

    def schedule(self, event_input_name, event_input_value, 
        host, port, endpoint):

        if event_input_name == 'INIT':
            self.flask_output_queue = Queue()
            self._controllable_server = ControllableServer(self.flask_output_queue, host, port, endpoint)                      
            self._controllable_server.start()
            return [None, event_input_value, None]
        elif event_input_name == 'READ':
            message_from_within_the_callback = self.flask_output_queue.get()
            print(message_from_within_the_callback)
            return [None, event_input_value, message_from_within_the_callback]
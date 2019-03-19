import threading

from queue import Queue
import logging
from websocket_server import WebsocketServer


class QAService:

    def __init__(self, q):
        self.name = ""
        self._q = q
        self._answer = ""

    def _run_thread(self):
        server = WebsocketServer(13254, host='127.0.0.1', loglevel=logging.INFO)
        server.set_fn_new_client(self.new_client)
        server.set_fn_message_received(self.message_recieved)
        server.run_forever()

    def new_client(self, client, server):
        # server.send_message_to_all("Hey all, a new client has joined us")
        print("new client has joined")

    def message_recieved(self, client, server, message):
        print("received message from client {}: {}".format(client, message))
        # answer = self.predict_answer(message)
        evt = threading.Event()
        self._q.put((message, evt))
        evt.wait()

        server.send_message(client, self._answer)

    def set_answer(self, answer):
        self._answer = answer

    def start_web_server(self):
        th = threading.Thread(target=self._run_thread)
        th.start()

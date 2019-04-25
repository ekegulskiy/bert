import threading
import logging
from websocket_server import WebsocketServer
""" WebSocket service 
Runs on a separate thread, supports multiple clients
"""
class QAService:
    def __init__(self, q):
        self.name = ""
        self._q = q
        self._answer = ""

    def _run_thread(self):
        # Initializes WebSocket for specific IP and PORT number
        server = WebsocketServer(13254, host='127.0.0.1', loglevel=logging.INFO)

        # assigns new_client callback function
        server.set_fn_new_client(self.new_client)

        # assigns callback for receving messages from clients
        server.set_fn_message_received(self.message_recieved)

        # starts main loop of WebSocket server
        server.run_forever()

    def new_client(self, client, server):
        # server.send_message_to_all("Hey all, a new client has joined us")
        print("new client has joined")

    def message_recieved(self, client, server, message):
        print("=======================================================================================================")
        print("NEW REQUEST FROM CLIENT: {}".format(client))
        print("DATA: {}".format(message))
        print("NUMBER OF TEXT TOKENS: {}".format(len(message.split())))
        # answer = self.predict_answer(message)
        evt = threading.Event()
        self._q.put((message, evt))

        # waits for processing thread to process the message
        evt.wait()

        # sends a message to client with processed result
        print("Sending message back {}".format(self._answer))
        server.send_message(client, self._answer)

    def set_answer(self, answer):
        # called by message processing thread to set the result
        self._answer = answer

    def start_web_server(self):
        # starts separate thread for running WebSocket server
        th = threading.Thread(target=self._run_thread)
        th.start()

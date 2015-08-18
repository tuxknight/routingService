#!/usr/bin/env python

import json
import os
import zmq

class Ctrl(object):
    def __init__(self, host, port, in_file):
        self.host = host
        self.port = port
        self.in_file = in_file
        self.out_file = os.path.basename("/var/log/bootstrap.log").replace("log","out")
        self.client_context = zmq.Context()
        self.client = self.client_context.socket(zmq.PAIR)

    def send(self):
        self.client.connect("tcp://%s:%d" % (self.host, self.port))
        message = self._args_to_json(self.in_file, self.out_file)
        print("Sending message: %s" % message)
        self.client.send(message)

    def _args_to_json(self, in_file, out_file):
        """
        Combines all arguments and return a JSON-style text.
        """
        # input
        arg1 = {"filename": in_file}
        arg2 = {"lines": 5}
        args = [arg1, arg2]
        _input = {}
        _input['name'] = "file"
        _input['arguments'] = args

        # exchange
        arg1 = {"sock": "/tmp/exchange.sock"}
        args = [arg1]
        _exchange = {}
        _exchange['name'] = "unixsocket"
        _exchange['arguments'] = args

        # output
        arg1 = {"filename": out_file}
        args = [arg1]
        _output = {}
        _output['name'] = "file"
        _output['arguments'] = args

        message = {}
        message['input'] = _input
        message['exchange'] = _exchange
        message['output'] = _output

        return json.dumps(message)

if __name__ == "__main__":
    controller = Ctrl("127.0.0.1", 6002, "/var/log/bootstrap.log")
    controller.send()

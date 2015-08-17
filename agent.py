#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
try:
    import json
    import zmq
except ImportError as e:
    logger.drs_log.fatal("%s" % e.message)
    sys.exit(1)

from routingService import logger


class Agent(object):
    def __init__(self, host="127.0.0.1", port=6003):
        self.context = zmq.Context()
        self.host = host
        self.port = port
        # self.client = self.context.socket(zmq.REQ)
        self.client = self.context.socket(zmq.PAIR)

    def start(self):
        self.client.connect("tcp://%s:%d" % (self.host, self.port))
        file_list = ["/var/log/syslog", "/var/log/auth.log", "/var/log/upstart/docker.log"]
        for f in file_list:
            request = self._args_to_json(f)
            logger.drs_log.debug("sending request: %s" % request)
            self.client.send(request)
            # logger.drs_log.debug(self.client.recv())

    def _args_to_json(self, filename):
        """
        Combines all arguments and return a JSON-style text.
        """
        # input
        target_file = filename
        arg1 = {"filename": target_file}
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
        arg1 = {"filename": "output.txt"}
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
    agent = Agent()
    agent.start()

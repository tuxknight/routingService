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
    def __init__(self, portal_host="127.0.0.1", portal_port=6003):
        # Create a socket as a server to receive commands from controller node
        # Also create a socket as a client to send command to Portal
        self.portal_context = zmq.Context()
        self.host = portal_host
        self.port = portal_port
        # self.portal_client = self.portal_context.socket(zmq.REQ)
        self.portal_client = self.portal_context.socket(zmq.PAIR)

        # receive controller message <demo>
        self.server_context = zmq.Context()
        self.server = self.server_context.socket(zmq.PAIR)
        self.server.bind("tcp://*:6002")
        logger.drs_log.debug("waiting for directives on port:6002")        

    def start(self):
        while True:
            self.request = self.server.recv()
            # adjust for running in docker container
            # connect by hostname, not IP address
            logger.drs_log.debug("try connecting to tcp://%s:%d" % (self.host, self.port))
            self.portal_client.connect("tcp://%s:%d" % (self.host, self.port))
            # use IP address if running on a host or VM
            # self.portal_client.connect("tcp://127.0.0.1:6003")
            logger.drs_log.debug("sending request: %s" % self.request)
            self.portal_client.send(self.request)
            logger.drs_log.debug("request finished.")
            logger.drs_log.debug(self.portal_client.recv())

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
        _exchange['name'] = "unixclient"
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
    # adjust for running in docker container
    agent = Agent(portal_host="portal")
    # if running on a host or VM, portal_host could be IP address
    # which set 127.0.0.1 as default
    # agent = Agent(portal_host="portal")
    # argument "portal" is the hostname of portal container.
    agent.start()

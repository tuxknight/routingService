#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
try:
    import json
    import zmq
except ImportError as e:
    logger.drs_log.fatal(e.message)
    sys.exit(1)

import logger
from entrypoint import EntryPoint

class Portal(object):
    def __init__(self, host="*", port=6003):
        """running as a server to receive commands from agent
        create entrypoint according to the arguments sent from agent
        """
        self.zmq_context = zmq.Context()
        self.host = host
        if self.host in ("0", "*"):
            self.host = "*"
        self.port = port
        # self.socket = self.zmq_context.socket(zmq.REP)
        self.socket = self.zmq_context.socket(zmq.PAIR)
        self.socket.bind("tcp://%s:%d" % (self.host, self.port))
        self.INPUT = "plugins.input"
        self.OUTPUT = "plugins.output"
        self.EXCHANGE = "plugins.exchange"
        logger.drs_log.debug("Server listening(tcp://%s:%d)" % (self.host, 
                                                                self.port))

    def worker(self):
        while True:
            message = self.socket.recv()
            logger.drs_log.debug("Received request: %s" % message)
            logger.drs_log.debug("Parsing message...")
            self.args_entrypoint = json.loads(message)
            self._parse_json()

            logger.drs_log.debug("Create EntryPoint")
            entry_point = EntryPoint(self.entrypoint_input,
                                     self.entrypoint_output,
                                     self.entrypoint_exchange)
            entry_point.start()

    def _parse_json(self):
        """extract arguments and combine them as arguments of EntryPoint
        """
        if len(self.args_entrypoint) is not 3:
            return -1
        # (plugin_name, plugin_arguments)
        self.entrypoint_input = (
                            self.INPUT+"."+
                            self.args_entrypoint["input"]["name"], 
                            self._extract_args(
                                self.args_entrypoint["input"]["arguments"]
                                )
                            )
        self.entrypoint_output = (
                             self.OUTPUT+"."+
                             self.args_entrypoint["output"]["name"], 
                             self._extract_args(
                                 self.args_entrypoint["output"]["arguments"]
                                 )
                            )
        self.entrypoint_exchange = (
                               self.EXCHANGE+"."+
                               self.args_entrypoint["exchange"]["name"], 
                               self._extract_args(
                                   self.args_entrypoint["exchange"]["arguments"]
                                   )
                            )

    def _extract_args(self, arg_list):
        """extract args from list and merge into one dict object"""
        result = {}
        for arg in arg_list:
            result = dict(arg.items()+result.items())
        return result

if __name__ == "__main__":
    portal = Portal()
    portal.worker()

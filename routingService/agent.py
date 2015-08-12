#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
try:
    import zmq
    import json
except ImportError as e:
    logger.drs_log.fatal("%s" % e.message)
    sys.exit(1)

import logger


context = zmq.Context()
server_ip = "127.0.0.1"
port = 6003
client = context.socket(zmq.REQ)
client.connect("tcp://%s:%d" % (server_ip, port))
# client.connect("tcp://%s:%d" % (server_ip2, port2))

logger.drs_log.debug("sending request...")
request = {"input_plugin": "plugins.input.file",
           "output_plugin": "plugins.output.file",
           "exchange_plugin": "plugins.exchange.unixsocket"}
client.send(request)
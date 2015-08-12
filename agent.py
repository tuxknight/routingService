#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
try:
    import zmq
    import json
except ImportError as e:
    logger.drs_log.fatal("%s" % e.message)
    sys.exit(1)

from routingService import logger


context = zmq.Context()
server_ip = "127.0.0.1"
port = 6003
client = context.socket(zmq.REQ)
client.connect("tcp://%s:%d" % (server_ip, port))
# client.connect("tcp://%s:%d" % (server_ip2, port2))

logger.drs_log.debug("sending request...")
request = {"input": "plugins.input.file",
           "output": "plugins.output.file",
           "exchange": "plugins.exchange.unixsocket"}
client.send(json.dumps(request))
logger.drs_log.debug(client.recv())


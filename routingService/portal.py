#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
try:
    import zmq
except ImportError:
    logger.drs_log.fatal("module ZeroMQ was required.")
    sys.exit(1)

import logger
from entrypoint import EntryPoint


zmq_context = zmq.Context()
port = 6003
socket = zmq_context.socket(zmq.REP)
socket.bind("tcp://*:%d" % port)

while True:
    message = socket.recv()
    logger.drs_log.debug("Received request: %s" % message)
    logger.drs_log.debug("Parsing message...")
    result = message.upper()
    socket.send(result)


# e = EntryPoint()

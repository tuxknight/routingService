#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
try:
    import zmq
except ImportError:
    logger.drs_log.fatal("module zeromq was required.")
    sysexit(1)

import logger
from entrypoint import EntryPoint

e = EntryPoint()

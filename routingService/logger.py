#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import logging.handlers
import sys

LOG_FILE = "/tmp/drs.log"
fmt = "%(name)s %(levelname)s %(asctime)s [ %(module)s(%(process)s):%(lineno)s:%(funcName)s ] %(message)s"
formatter = logging.Formatter(fmt)
rotation_handler = logging.handlers.RotatingFileHandler(LOG_FILE,
                                                        maxBytes=1024*1024,
                                                        backupCount=5)
std_handler = logging.StreamHandler(sys.stdout)

rotation_handler.setFormatter(formatter)
std_handler.setFormatter(formatter)

rotation_handler.setLevel(logging.DEBUG)
std_handler.setLevel(logging.DEBUG)

drs_log = logging.getLogger("drs")
drs_log.addHandler(rotation_handler)
drs_log.setLevel(logging.DEBUG)
drs_log.addHandler(std_handler)

#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import BaseInput
from subprocess import PIPE
from subprocess import Popen
import logger


class FileIn(BaseInput):
    def run(self):
        """deal with input type: file
        return data"""
        logger.drs_log.debug("plugin:input/file")
        return self.read("/var/log/syslog", 5)

    def read(self, filename, lines):
        return Popen(["tail", "-n%d" % lines, filename],
                     stdout=PIPE).communicate()[0]


def inject_plugin():
    return FileIn

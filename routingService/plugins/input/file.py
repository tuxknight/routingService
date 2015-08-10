#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import BaseInput
from subprocess import PIPE
from subprocess import Popen
import logger


class FileIn(BaseInput):
    def __init__(self):
        super(FileIn, self).__init__()
        logger.drs_log.debug("plugin:input/file")

    def run(self, filename, lines):
        """deal with input type: file
        return data"""
        self.filename = filename
        self.lines = lines
        return self.read(self.filename, self.lines)

    def read(self, filename, lines):
        return Popen(["tail", "-n%d" % lines, filename],
                     stdout=PIPE).communicate()[0]


def inject_plugin():
    return FileIn

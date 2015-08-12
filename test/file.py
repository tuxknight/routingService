#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import BaseInput
from subprocess import PIPE
from subprocess import Popen
import logger


class FileIn(BaseInput):
    """{"module": "input",
        "name": "file",
        "author": "Fuyuan.Chu <fuyuan.chu@emc.com>",
        "version": "0.1",
        "desc": "read last lines of filename",
        "options": [
             {"option": "filename",
              "required": "True",
              "desc": "name of the file which be read"
             },
             {"option": "lines",
              "required": "False",
              "default": 5,
              "desc": "last lines should be read"
             }
        ]
    }
    """
    def __init__(self, filename, lines=5):
        super(FileIn, self).__init__()
        self.filename = filename
        self.lines = lines
        logger.drs_log.debug("plugin:input/file")

    def run(self):
        """deal with input type: file
        return data"""
        return self.read(self.filename, self.lines)

    def read(self, filename, lines):
        return Popen(["tail", "-n%d" % lines, filename],
                     stdout=PIPE).communicate()[0]


def inject_plugin():
    return FileIn

#!/usr/bin/env python

from . import BaseOutput
import logger


class FileOutput(BaseOutput):
    """{"module": "output",
        "name": "file",
        "author": "Fuyuan.Chu <fuyuan.chu@emc.com>",
        "version": "0.1",
        "desc": "write result to local file",
        "options": [
             {"option": "filename",
              "required": "True",
              "desc": "file which result will be written to",
              "default": "output.txt"
             }
        ]
    }
    """
    def __init__(self, filename="output.txt"):
        super(FileOutput, self).__init__()
        self.filename = filename
        logger.drs_log.debug("plugin: output/FileOutput")

    def run(self, data):
        """deal with output type: File
        send data"""
        self.write(self.filename, data)

    def write(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)


def inject_plugin():
    return FileOutput

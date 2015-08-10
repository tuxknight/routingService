#!/usr/bin/env python

from . import BaseOutput
import logger


class FileOutput(BaseOutput):
    def __init__(self):
        super(FileOutput, self).__init__()
        logger.drs_log.debug("plugin: output/FileOutput")

    def run(self, data):
        """deal with output type: File
        send data"""
        self.write("output.txt", data)

    def write(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)


def inject_plugin():
    return FileOutput

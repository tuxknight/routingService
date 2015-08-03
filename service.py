#!/usr/bin/env python

from subprocess import PIPE
from subprocess import Popen


class BaseMService(object):
    def __init__(self):
        pass

    def read(self):
        pass

    def deal_with(self):
        pass

    def write(self):
        pass


class MService(BaseMService):
    def __init__(self):
        self.data = ""
        self.result = ""

    def read(self, filename, lines):
        self.data = Popen(['tail', '-n%d' % 5, filename],
                          stdout=PIPE).communicate()[0]

    def deal_with(self):
        if self.data:
            self.result = self.data.upper()
        else:
            return 1

    def write(self):
        if self.result:
            print(self.result.rstrip("\n"))


if __name__ == "__main__":
    service = MService()
    service.read("/var/log/syslog", 5)
    service.deal_with()
    service.write()

#!/usr/bin/env python

from twisted.internet import reactor
import traceback

class Countdown(object):
    counter = 5

    def count(self):
        if self.counter == 0:
            reactor.stop()
        else:
            self.counter -= 1
            reactor.callLater(1, self.count)

reactor.callWhenRunning(Countdown().count)
print("Start")
reactor.run()
print("Stop")

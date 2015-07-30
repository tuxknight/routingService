#!/usr/bin/env python
#


class BaseDealWith(object):
    def __init__(self, style):
        pass

    def in(self):
        pass

    def to_service(self):
        pass

    def from_service(self):
        pass

    def out(self):
        pass


class DealWithFile(BaseDealWith):
    def __init__(self, style):
        pass

    def in(self):
        pass

    def to_service(self):
        pass

    def from_service(self):
        pass

    def out(self):
        pass


class DealWithTCP(BaseDealWith):
    pass


class DealWithHttp(BaseDealWith):
    pass


class DealWithUDP(BaseDealWith):
    pass

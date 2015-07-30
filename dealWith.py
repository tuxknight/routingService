class InteractWithService:
    def __init__(self)
        pass

    def to_service(self):
        pass

    def from_service(self):
        pass

class InteractWithRouting:
    def __init__(self,style):
        pass

    def in(self):
        pass

    def out(self):
        pass


class BaseDealWith(InteractWithService,InteractWithRouting):

    def __init__(self, style):
       print ' '


class DealWithFile(BaseDealWith):

    def __init__(self,style):

    def in(self):

    def to_service(self):

    def from_service(self):

    def out(self):


class DealWithTCP(BaseDealWith):


class DealWithHttp(BaseDealWith):


class DealWithUDP(BaseDealWith):

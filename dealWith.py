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

    def from_routing(self):
        pass

    def to_routing(self):
        pass


class BaseDealWith(InteractWithService,InteractWithRouting):
    def __init__(self, style):
        pass


class DealWithFile(BaseDealWith):
    def __init__(self, style):
        pass

    def from_routing(self):
        pass

    def to_service(self):
        pass

    def from_service(self):
        pass

    def to_routing(self):
        pass


class DealWithTCP(BaseDealWith):


class DealWithHttp(BaseDealWith):


class DealWithUDP(BaseDealWith):

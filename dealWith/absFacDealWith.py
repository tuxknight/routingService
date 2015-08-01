from interactWithRouting import InteractWithRouting


class InteractWithService(object):
    def __init__(self):
        pass

    def to_service(self):
        pass

    def from_service(self):
        pass


class Service(InteractWithRouting,InteractWithService):
    def __init__(self,style1,style2):
 	self.From_routing = InteractWithRouting(style1)
	self.To_routing = InteractWithRouting(style2)
 	pass

    def from_routing(self):
        self.From_routing.from_routing()
	pass

    def to_routing(self):
	self.To_routing.to_routing()
        pass

    def to_service(self):
        pass

    def from_service(self):
        pass

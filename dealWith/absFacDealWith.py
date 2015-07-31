class InteractWithRouting(object):
    def __init__(self,style1,style2):
	pass

    def from_routing(self,style1):
	pass

    def to_routing(self,style2):
	pass


class InteractWithService(object):
    def __init__(self)
        pass

    def to_service(self):
        pass

    def from_service(self):
        pass


class ServiceProduct(InteractWithRouting,InteractWithService):
    def __init__(self,style1,style2):
        InteractWithRouting.__init__(self,style1,style2)
	InteractWithService.__init__(self)
 	pass


class Service(ServiceProduct):
    def __init__(self,style1,style2):
        ServiceProduct.__init__(self,style1,style2)
        pass

    def from_routing(self,style1):
        pass

    def to_routing(self,style2):
        pass

    def to_service(self):
        pass

    def from_service(self):
        pass

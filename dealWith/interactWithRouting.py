class InteractWithRouting(object):
    def __init__(self,style):
	self.style = style
        if self.style == 'file':
	    self.DealWith = FileDealWith()
	elif self.style == 'TCP':
	    self.DealWith = TCPDealWith()
	elif self.style == 'HTTP':
	    self.DealWith = HTTPDealWith()
	pass

    def from_routing(self):
	self.DealWith.from_routing()
        pass

    def to_routing(self):
	self.DealWith.to_routing()
        pass


class TCPDealWith(InteractWithRouting):
    def __init__(self):
        pass

    def from_routing(self):
	print 'tcp from routing'
        pass

    def to_routing(self):
	print 'tcp to routing'
        pass


class HTTPDealWith(InteractWithRouting):
    def __init__(self):
        pass

    def from_routing(self):
	print 'http from routing'
        pass

    def to_routing(self):
	print 'http to routing'
        pass


class FileDealWith(InteractWithRouting):
    def __init__(self):
        pass

    def from_routing(self):
	print 'file from routing'
        pass

    def to_routing(self):
	print 'file to routing'
        pass

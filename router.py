from device import Device

class RoutingTable():
    """A simple routing table class. This is essentially a
       dictionary that maps an identifier to a link.

    Attributes:
        table: The dictionary (identifier string, Link)
    """

    def __init__(self):
        self.table = {}


class Router(Device):
    """A router

    Attributes:
        identifier: The unique identification of the router
        routing_table: The instance of RoutingTable
    """

    def __init__(self, identifier):
        Device.__init__(self, identifier)
        self.routing_table = RoutingTable()
        self.links = []

    def __str__(self):
        return ("Router ID  " + self.identifier + "\n")

    # Called by links in response to to forward packet to a
    # given destination
    def handle_packet(self, packet):
        # Get packet destination from packet and decide
        # where to send packet next
        # Should calculate routing tables with decentralized
        # shortest path algorithm
        pass

    # Called during parsing to set up object graph
    def attach_link(self, link):
        self.links.append(link)
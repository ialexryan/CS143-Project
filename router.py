import sys
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

    # Called internally by routers to forward packets
    # and called externally by flows to initiate packet sending
    def send_packet(self, packet):
        # Get packet destination from packet and decide
        # where to send packet next
        # Should calculate routing tables with decentralized
        # shortest path algorithm
        pass

    # Exclusively called by links to deliver packets
    def receive_packet(self, packet):
        pass

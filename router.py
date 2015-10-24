from device import Device

class Router(Device):
    """A router

    Attributes:
        identifier: The unique identification of the router
    """

    def __init__(self, identifier):
        Device.__init__(self, identifier)

    # Called internally by routers to forward packets
    def send_packet(self, packet):
        # Get packet destination from packet and decide
        # where to send packet next
        # Should calculate routing tables with decentralized
        # shortest path algorithm
        pass

    # Exclusively called by links to deliver packets
    def receive_packet(self, packet):
        pass

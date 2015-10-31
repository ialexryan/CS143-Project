class Packet:
    """A generic network packet.

    Attributes:
        source: The host that sent the packet
        destination: The host to which the packet was sent
        packet_type: The packet type
        size: The packet size, in bytes
    """

    def __init__(self, source, destination, size):
        self.source = source
        self.destination = destination
        self.size = size

    def __str__(self):
        return ("Packet\n"
                "source:      " + self.source.identifier + "\n"
                "destination: " + self.destination.identifier + "\n"
                "size:        " + str(self.size) + " bytes\n")


class RoutingPacket(Packet):
    """A routing packet. It contains routing tables and
       is used by routers to communicate with each other.
       Routing packets bypass the link buffer and aren't
       logged.

    Attributes:
        routing_table: the RoutingTable"""

    def __init__(self, source, destination, size, routing_table):
        Packet.__init__(self, source, destination, size)
        self.routing_table = routing_table

    def __str__(self):
        return ("RoutingPacket\n"
                "source:      " + self.source.identifier + "\n"
                "destination: " + self.destination.identifier + "\n"
                "size:        " + str(self.size) + " bytes\n")

class Packet:
    """A generic network packet.
       Superclass of StandardPacket and RoutingPacket.

    Attributes:
        source: The host that sent the packet
        destination: The host to which the packet was sent
        packet_type: The packet type
        size: The packet size, in bytes
    """

    def __init__(self, size):
        self.size = size

    def __str__(self):
        return ("Packet\n"
                "source:      " + self.source.identifier + "\n"
                "destination: " + self.destination.identifier + "\n"
                "size:        " + str(self.size) + " bytes\n")

class StandardPacket(Packet):
    """A packet for sending information between hosts on the network.
       Superclass of PayloadPacket and AcknowledgementPacket.

    Attributes:
        identifier: the packet ID that a pair of Payload and ACK packets share
        source: The host that sent the packet
        destination: The host to which the packet was sent
        size: The packet size, in bytes
    """
    
    def __init__(self, identifier, source, destination, size):
        Packet.__init__(self, size)
        self.identifier = identifier
        self.source = source
        self.destination = destination

    def __str__(self):
        return ("StandardPacket ID " + self.identifier + "\n"
                "source:           " + self.source.identifier + "\n"
                "destination:      " + self.destination.identifier + "\n"
                "size:             " + str(self.size) + " bytes\n")

class PayloadPacket(StandardPacket):
    """A packet for sending information to another host on the network.

    Attributes:
        source: The host that sent the packet
        destination: The host to which the packet was sent
        size: The packet size, in bytes
    """
    
    def __init__(self, identifier, source, destination):
        StandardPacket.__init__(self, identifier, source, destination, 1024)

    def acknowledgement(self):
        return AcknowledgementPacket(self.identifier, self.destination, self.source)

    def __str__(self):
        return ("PayloadPacket ID " + self.identifier + "\n"
                "source:          " + self.source.identifier + "\n"
                "destination:     " + self.destination.identifier + "\n"
                "size:            " + str(self.size) + " bytes\n")

class AcknowledgementPacket(StandardPacket):
    """A packet for acknowledging receipt of a PayloadPacket
       from another host on the network.

    Attributes:
        source: The host that sent the packet
        destination: The host to which the packet was sent
        size: The packet size, in bytes
    """
    
    def __init__(self, identifier, source, destination):
        StandardPacket.__init__(self, identifier, source, destination, 64)

    def __str__(self):
        return ("AcknowledgementPacket ID " + self.identifier + "\n"
                "source:                  " + self.source.identifier + "\n"
                "destination:             " + self.destination.identifier + "\n"
                "size:                    " + str(self.size) + " bytes\n")

class RoutingPacket(Packet):
    """A packet for communicating routing information between routers on
       the network such that routing tables can be updated in a distributed
       manner.

    Attributes:
        source: The host that sent the packet
        timestamp: The time at which the host sent the packet
        size: The packet size, in bytes
    """
    
    def __init__(self, source, timestamp):
        Packet.__init__(self, 64)
        self.source = source
        self.timestamp = timestamp

    def __str__(self):
        return ("RoutingPacket\n"
                "source:      " + self.source.identifier + "\n"
                "timestamp: " + str(self.timestamp) + "\n"
                "size:        " + str(self.size) + " bytes\n")

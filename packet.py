class PacketType:
    """A simple class that represents the various packet types"""

    # placeholders (I'm not sure what packet types we'll end up needing)
    TYPEA = "TYPEA"
    TYPEB = "TYPEB"


class Packet:
    """A network packet.

    Attributes:
        source: The host that sent the packet
        destination: The host to which the packet was sent
        packet_type: The packet type
        size: The packet size, in bytes
    """

    def __init__(self, source, destination, packet_type, size):
        self.source = source
        self.destination = destination
        self.packet_type = packet_type
        self.size = size

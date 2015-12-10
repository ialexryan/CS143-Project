class StandardPacket():
    """A packet for sending information between hosts on the network.
       Superclass of PayloadPacket and AcknowledgementPacket.

    Attributes:
        identifier: the packet ID that a pair of Payload and ACK packets share
        duplicate_num: Which duplicate of the original packet this packet is
        flowID: The flow that sent the packet
        source: The host that sent the packet
        destination: The host to which the packet was sent
        size: The packet size, in bytes
    """

    def __init__(self, identifier, duplicate_num, flow_id, source, destination, size):
        self.size = size
        self.identifier = identifier
        self.duplicate_num = duplicate_num
        self.flow_id = flow_id
        self.source = source
        self.destination = destination


class PayloadPacket(StandardPacket):
    """A packet for sending information to another host on the network.

    Attributes:
        identifier: The packet number sent by a flow
        duplicate_num: Which duplicate of the original packet this packet is
        flow_id: The flow that sent the packet
        source: The host that sent the packet
        destination: The host to which the packet was sent
        size: The packet size, in bytes
    """

    def __init__(self, identifier, duplicate_num, flow_id, source, destination, payload_size, ack_size):
        StandardPacket.__init__(self, identifier, duplicate_num, flow_id, source, destination, payload_size)
        self.ack_size = ack_size

    def acknowledgement(self, next_id):
        return AcknowledgementPacket(self.identifier, self.duplicate_num, next_id, self.flow_id, self.destination, self.source, self.size, self.ack_size)

    def __str__(self):
        return ("PayloadPacket #" + str(self.identifier) + "\n"
                "Duplicate #    " + str(self.duplicate_num) + "\n"
                "flowID:        " + self.flow_id + "\n"
                "source:        " + self.source.identifier + "\n"
                "destination:   " + self.destination.identifier + "\n"
                "size:          " + str(self.size) + " bytes\n")


class AcknowledgementPacket(StandardPacket):
    """A packet for acknowledging receipt of a PayloadPacket
       from another host on the network.

    Attributes:
        identifier: The packet number sent by a flow
        duplicate_num: Which duplicate of the original packet this packet is
        next_id: ID of next expected packet
        flow_id: The flow that sent the packet
        source: The host that sent the packet
        destination: The host to which the packet was sent
        size: The packet size, in bytes
    """

    def __init__(self, identifier, duplicate_num, next_id, flow_id, source, destination, payload_size, ack_size):
        StandardPacket.__init__(self, identifier, duplicate_num, flow_id, source, destination, ack_size)
        self.payload_size = payload_size
        self.next_id = next_id

    def __str__(self):
        return ("AcknowledgementPacket #" + str(self.identifier) + "\n"
                "Duplicate #            " + str(self.duplicate_num) + "\n"
                "flowID:                " + self.flow_id + "\n"
                "source:                " + self.source.identifier + "\n"
                "destination:           " + self.destination.identifier + "\n"
                "size:                  " + str(self.size) + " bytes\n")

class RoutingPacket:
    """A packet for communicating routing information between routers on
       the network such that routing tables can be updated in a distributed
       manner.

    Attributes:
        source: The host that sent the packet
        timestamp: The time at which the host sent the packet
        size: The packet size, in bytes
    """

    def __init__(self, source, timestamp, size):
        self.size = size
        self.source = source
        self.timestamp = timestamp

    def __str__(self):
        return ("RoutingPacket\n"
                "source:      " + self.source.identifier + "\n"
                "timestamp: " + str(self.timestamp) + "\n"
                "size:        " + str(self.size) + " bytes\n")

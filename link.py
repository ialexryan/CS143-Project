class Buffer:
    """A buffer that holds packets that are waiting to send.
        
        """
    
    def __init__(self):
        pass

class Link:
    """A network link from A to B.

    Attributes:
        identifier: The unique identification of the link
        capacity: The rate at which the link sends packets
        delay: The transmission delay between ends of the link
        bufferA: The buffer storing packets from A to be sent to B
        bufferB: The buffer storing packets from B to be sent to A
    """

    def __init__(self, identifier, capacity, deviceA, deviceB):
        self.identifier = identifier
        self.capacity = capacity
        self.bufferA = Buffer()
        self.bufferB = Buffer()
        self.deviceA = deviceA
        self.deviceB = deviceB

    # It is illegal but not enforced to send a packet
    # from a device that isn't connected to this link
    def sendPacket(self, packet, toDevice):
        pass

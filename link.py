class Buffer:
    """A buffer that holds packets that are waiting to send.

    Attributes:
        size: The size of the buffer in KB
    """

    def __init__(self, size):
        self.size = size

class Link:
    """A network link from A to B.

    Attributes:
        identifier: The unique identification of the link
        capacity: The rate at which the link sends packets in mbps
        delay: The transmission delay between ends of the link in ms
        buffer: The Buffer storing packets
        deviceA: instance of Device
        deviceB: instance of Device
    """

    def __init__(self, identifier, rate, delay, buffer_size, deviceA, deviceB):
        self.identifier = identifier
        self.rate = rate
        self.delay = delay
        self.buffer = Buffer(buffer_size)
        self.deviceA = deviceA
        self.deviceB = deviceB

    def __str__(self):
        return ("Link ID   " + self.identifier + "\n"
                "rate:     " + str(self.rate) + " mbps\n"
                "delay:    " + str(self.delay) + " ms\n"
                "buffer:   " + str(self.buffer.size) + " KB\n"
                "device A: " + self.deviceA.identifier + "\n"
                "device B: " + self.deviceB.identifier) + "\n"

    # It is illegal but not enforced to send a packet
    # from a device that isn't connected to this link
    def sendPacket(self, packet, toDevice):
        pass

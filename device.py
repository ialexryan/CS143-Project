import sys

class Device:
    """A network device

    Attributes:
        identifier: The unique identification of the device
    """

    def __init__(self, identifier):
        self.identifier = identifier

    # Called on device to pass along packet, and device
    # will use contents of the packet to decide what to do
    def handle_packet(self, packet):
        sys.exit("Abstract method handle_packet not implemented")

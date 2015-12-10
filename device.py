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
    def handle_packet(self, packet, from_link):
        sys.exit("Abstract method handle_packet not implemented")

    # Called during parsing to set up object graph
    def attach_link(self, link):
        sys.exit("Abstract method attach_link not implemented")

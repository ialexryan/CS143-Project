import sys

class Device:
    """A network device

    Attributes:
        identifier: The unique identification of the device
    """

    def __init__(self, identifier):
        self.identifier = identifier

    # Called internally by routers to forward packets
    # and called externally by flows to initiate packet sending
    def send_packet(self, packet):
        sys.exit("Abstract method send_packet not implemented")

    # Exclusively called by links to deliver packets
    def receive_packet(self, packet):
        sys.exit("Abstract method send_packet not implemented")

import sys
from device import Device

class Host(Device):
    """A host

    Attributes:
        identifier: The unique identification of the host
    """

    def __init__(self, identifier):
        Device.__init__(self, identifier)

    def send_packet(self, packet):
        pass

    def receive_packet(self, packet):
        pass

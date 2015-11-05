from device import Device

class Host(Device):
    """A host

    Attributes:
        identifier: The unique identification of the host
    """

    def __init__(self, identifier):
        Device.__init__(self, identifier)

    def __str__(self):
        return ("Host ID  " + self.identifier + "\n")

    # Called by flow to send payload and called by links
    # in response to events in the event queue
    def handle_packet(self, packet):
        # - If this packet is an acknowledgment packet,
        #   notify flow so it can do the bookkeeping
        # - If this packet is a payload packet, respond
        #   by sending an acknowledgement packet across
        #   the same link
        pass

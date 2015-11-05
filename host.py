from device import Device
from packet import PayloadPacket, AcknowledgementPacket
import sys

class Host(Device):
    """A host

    Attributes:
        identifier: The unique identification of the host
    """

    def __init__(self, identifier):
        Device.__init__(self, identifier)
        self.link = None

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
        if isinstance(packet, PayloadPacket):
            print "Host: Sending packet"
            self.link.send_packet(packet, self)
        elif isinstance(packet, AcknowledgementPacket):
            print "Host: Receiving acknowledgement"
        else:
            sys.exit("Unknown packet type")

    # Called during parsing to set up object graph
    def attach_link(self, link):
        if self.link == None:
            self.link = link
        else:
            sys.exit("Illegal to attach multiple links to a host")
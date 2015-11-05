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
        self.flow = None

    def __str__(self):
        return ("Host ID  " + self.identifier)

    # Called by flow to send payload and called by links
    # in response to events in the event queue
    def handle_packet(self, packet):
        if packet.destination == self:
            # - If this packet is an acknowledgment packet,
            #   notify flow so it can do the bookkeeping
            # - If this packet is a payload packet, respond
            #   by sending an acknowledgement packet across
            #   the same link
            if isinstance(packet, PayloadPacket):
                self.link.send_packet(packet.acknowledgement(), self)
            elif isinstance(packet, AcknowledgementPacket):
                self.flow.receive_acknowledgement(packet)
            else:
                sys.exit("Unknown packet type")
        elif packet.source == self:
            # Send packet across link
            self.link.send_packet(packet, self)
        else:
            sys.exit("Illegal for host to handle a packet that it is neither source or destination of")

    # Called during parsing to set up object graph
    def attach_link(self, link):
        if self.link == None:
            self.link = link
        else:
            sys.exit("Illegal to attach multiple links to a host")
from device import Device
from packet import PayloadPacket, AcknowledgementPacket, RoutingPacket
from event import RoutingUpdateEvent
import sys

ROUTING_UPDATE_PERIOD = 100000

class Host(Device):
    """A host

    Attributes:
        identifier: The unique identification of the host
        flow: the Flow sending and receiving through this host
    """

    def __init__(self, identifier):
        Device.__init__(self, identifier)
        self.link = None
        self.flow = None
        self.clock = None
        self.event_scheduler = None

    def __str__(self):
        return ("Host ID  " + self.identifier)

    def send_packet(self, packet):
        assert packet.source == self
        # Send packet across link
        self.link.send_packet(packet, self)

    def receive_packet(self, packet):
        assert packet.destination == self
        # - If this packet is an acknowledgment packet,
        #   notify flow so it can do the bookkeeping
        # - If this packet is a payload packet, respond
        #   by sending an acknowledgement packet across
        #   the same link
        if isinstance(packet, PayloadPacket):
            self.link.send_packet(packet.acknowledgement(), self)
        elif isinstance(packet, AcknowledgementPacket):
            self.flow.acknowledgement_received(packet)
        else:
            sys.exit("Host doesn't know how to receive packet of type " + type(packet).__name__)

    # Called by flow to send payload and called by links
    # in response to events in the event queue
    def handle_packet(self, packet, from_link):
        if hasattr(packet, 'destination') and packet.destination == self:
            self.receive_packet(packet)
        elif hasattr(packet, 'source') and packet.source == self:
            self.send_packet(packet)
        elif isinstance(packet, RoutingPacket):
            pass # Should only happen if two hosts are directly connected by a link
        else:
            sys.exit("Host doesn't know how to handle packet that neither originates from or is directed to self")

    # Called during parsing to set up object graph
    def attach_link(self, link):
        if self.link == None:
            self.link = link
        else:
            sys.exit("Illegal to attach multiple links to a host")

    # Called by RoutingUpdateEvent to trigger sending a routing packet,
    # and then reschedules a RoutingUpdateEvent
    def send_routing_packet(self):
        self.send_packet(RoutingPacket(self, self.clock.current_time, 64))
        self.event_scheduler.delay_event(ROUTING_UPDATE_PERIOD, RoutingUpdateEvent(self))

import sys
from device import Device
from packet import StandardPacket, PayloadPacket, AcknowledgementPacket, RoutingPacket
from event import RoutingUpdateEvent
from packet_tracker import PacketTracker
import sys

ROUTING_UPDATE_PERIOD = 100000  #Every 100 seconds?? That's a long time...

class Host(Device):
    """A host

    Attributes:
        identifier: The unique identification of the host
        flow: the Flow sending and receiving through this host
    """

    def __init__(self, identifier):
        Device.__init__(self, identifier)
        self.link = None
        self.flows = {}
        self.clock = None
        self.event_scheduler = None
        self.logger = None
        self.payload_packet_trackers = {}

    def __str__(self):
        return "Host ID  " + self.identifier

    def set_logger(self, logger):
        self.logger = logger

    def send_packet(self, packet):
        assert packet.source == self
        # Send packet across link
        self.link.send_packet(packet, self)

    def _payload_received(self, packet):
        assert isinstance(packet, PayloadPacket)
        if packet.flow_id not in self.payload_packet_trackers:
            self.payload_packet_trackers[packet.flow_id] = PacketTracker()
        ack_tracker = self.payload_packet_trackers[packet.flow_id]
        ack_tracker.account_for_packet(packet.identifier)
        return packet.acknowledgement(ack_tracker.next_packet)


    # Called by flow to send payload and called by links
    # in response to events in the event queue
    def handle_packet(self, packet, from_link):
        if isinstance(packet, RoutingPacket):
            return # Should only happen if two hosts are directly connected by a link

        assert isinstance(packet, StandardPacket)
        assert packet.destination == self
        # - If this packet is an acknowledgment packet,
        #   notify flow so it can do the bookkeeping
        # - If this packet is a payload packet, respond
        #   by sending an acknowledgement packet across
        #   the same link
        if isinstance(packet, PayloadPacket):
            ack_packet = self._payload_received(packet)
            self.link.send_packet(ack_packet, self)
        elif isinstance(packet, AcknowledgementPacket):
            self.flows[packet.flow_id].acknowledgement_received(packet)
        else:
            sys.exit("Host doesn't know how to handle packet of type " + type(packet).__name__)

    # Called during parsing to set up object graph
    def attach_link(self, link):
        if self.link is None:
            self.link = link
        else:
            sys.exit("Illegal to attach multiple links to a host")

    # Called by RoutingUpdateEvent to trigger sending a routing packet,
    # and then reschedules a RoutingUpdateEvent
    def send_routing_packet(self):
        self.send_packet(RoutingPacket(self, self.clock.current_time, 64))
        self.event_scheduler.delay_event(ROUTING_UPDATE_PERIOD, RoutingUpdateEvent(self))

import sys
from device import Device
from packet import StandardPacket, PayloadPacket, AcknowledgementPacket, RoutingPacket
from event import RoutingUpdateEvent
from packet_tracker import PacketTracker
import sys

"""The wait time, in milliseconds, between sending out each routing update packet"""
ROUTING_UPDATE_PERIOD = 3000

class Host(Device):
    """A host

    Attributes:
        identifier: The unique identification of the host
        link: The Link that is attached to the host
        flows: An dictionary of the flows associated with a given host, keyed by identifier
        clock: The global clock used by the simulation
        event_schedluer: The event_scheduler that is used to schedule events 
        logger: The global logger
        payload_packet_trackers: A dictionary of trackers used to tracked received
            payload packets, keyed by flow identifier
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

    """Send a packet across the link attached to the host."""
    def send_packet(self, packet):
        assert packet.source == self
        # Send packet across link
        self.link.send_packet(packet, self)

    """Account for the received payload packet, and send a suitable acknlowedgmenet."""
    def _payload_received(self, packet):
        assert isinstance(packet, PayloadPacket)
        if packet.flow_id not in self.payload_packet_trackers:
            self.payload_packet_trackers[packet.flow_id] = PacketTracker()
        ack_tracker = self.payload_packet_trackers[packet.flow_id]
        ack_tracker.account_for_packet(packet.identifier)
        return packet.acknowledgement(ack_tracker.next_packet)

    """Called to deliver a packet to this host.
       RoutingPackets are ignored; StandardPackets are delivered to the host."""
    def handle_packet(self, packet, from_link):
        if isinstance(packet, RoutingPacket):
            # Should only happen if two hosts are directly connected by a link
            # since Routers don't forward routing packets to Hosts.
            return

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

    """Called during parsing to set up network graph."""
    def attach_link(self, link):
        if self.link is None:
            self.link = link
        else:
            sys.exit("Illegal to attach multiple links to a host")

    """Called by RoutingUpdateEvent to trigger sending a routing packet,
       and then reschedules a RoutingUpdateEvent."""
    def send_routing_packet(self):
        self.send_packet(RoutingPacket(self, self.clock.current_time, 64))
        self.event_scheduler.delay_event(ROUTING_UPDATE_PERIOD, RoutingUpdateEvent(self))

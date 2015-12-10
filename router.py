import sys
from device import Device
from packet import StandardPacket, RoutingPacket

class RoutingTable():
    """A table that records which link ought to be used for a given host
       and can be updated based on new routing packets.

    Attributes:
        _table: The dictionary mapping host_identifier to the tuple (timestamp, link)
    """

    def __init__(self):
        self._table = {}

    def get_entry(self, host_identifier):
        if host_identifier in self._table:
            return self._table[host_identifier][1]
        else:
            return None

    def _update_entry(self, host_identifier, timestamp, link):
        self._table[host_identifier] = (timestamp, link)

    # Returns true when the information updated the routing table
    def update_entry(self, host_identifier, timestamp, link):
        if host_identifier not in self._table:
            self._update_entry(host_identifier, timestamp, link)
            return True
        else:
            (old_timestamp, _) = self._table[host_identifier]
            if timestamp > old_timestamp:
                self._update_entry(host_identifier, timestamp, link)
                return True
            else:
                return False

class Router(Device):
    """A device that routes packets based on its routing table.

    Attributes:
        identifier: The unique identification of the router
        routing_table: The instance of RoutingTable
        logger: the Logger to be used
    """

    def __init__(self, identifier):
        Device.__init__(self, identifier)
        self.routing_table = RoutingTable()
        self.links = []
        self.logger = None

    def __str__(self):
        return "Router ID  " + self.identifier + "\n"

    def set_logger(self, logger):
        self.logger = logger

    """Update the routing table, and forward the routing packet over the proper links, if necessary."""
    def _handle_routing_packet(self, packet, from_link):
        assert isinstance(packet, RoutingPacket)
        previous_link = self.routing_table.get_entry(packet.source) # Used for logging
        if self.routing_table.update_entry(packet.source.identifier, packet.timestamp, from_link):
            if from_link is not previous_link:
                self.logger.log_updated_routing_table(self.identifier, packet.source.identifier, from_link.identifier, packet.timestamp)
            for link in self.links:
                if link is not from_link:
                    link.send_packet(packet, self)

    """Forward the packet over the correct link as determined by the routing table."""
    def _handle_standard_packet(self, packet):
        assert isinstance(packet, StandardPacket)
        dest = packet.destination
        link = self.routing_table.get_entry(dest.identifier)
        if link is not None:
            self.logger.log_router_sending_packet(self.identifier, packet, link.identifier)
            link.send_packet(packet, self)
        else:
            self.logger.log_router_dropped_packet_unknown_path(self.identifier, packet)

    """Deliever a packet over `from_link` to the router for forwarding."""
    def handle_packet(self, packet, from_link):
        if isinstance(packet, StandardPacket):
            self._handle_standard_packet(packet)
        elif isinstance(packet, RoutingPacket):
            self._handle_routing_packet(packet, from_link)
        else:
            sys.exit("Router doesn't know how to handle packet of type " + type(packet).__name__)

    # Called during parsing to set up object graph
    def attach_link(self, link):
        self.links.append(link)

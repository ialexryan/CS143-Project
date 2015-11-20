from device import Device

class RoutingTable():
    """A simple routing table class. This is essentially a
       dictionary that maps an identifier to a link.

    Attributes:
        table: The dictionary (identifier string, Link)
    """

    def __init__(self):
        self.table = {}
    
    def get_entry(self, identifier):
        return self.table.get(identifier)
            
    def set_entry(self, identifier, link):
        self.table[identifier] = link    


class Router(Device):
    """A router

    Attributes:
        identifier: The unique identification of the router
        routing_table: The instance of RoutingTable
    """

    def __init__(self, identifier):
        Device.__init__(self, identifier)
        self.routing_table = RoutingTable()
        self.links = []

    def __str__(self):
        return ("Router ID  " + self.identifier + "\n")

    # Called by links in response to to forward packet to a
    # given destination
    def handle_packet(self, packet):
        # Get packet destination from packet and decide
        # where to send packet next
        # Should calculate routing tables with decentralized
        # shortest path algorithm
                
        # Use static routing
        dest = packet.destination
        link = self.routing_table.get_entry(dest.identifier)
        self.logger.log_router_sending_packet(self.identifier, packet, link.identifier)
        link.send_packet(packet, self)

    # Called during parsing to set up object graph
    def attach_link(self, link):
        self.links.append(link)

    # Called during parsing to add an entry to the routing table
    # for hardcoded static routing
    def add_table_entry(self, destination, link):
        self.routing_table.set_entry(destination, link)

"""
    flow started event
    flow ended event
    flow sends packet
    flow receives packet
    link receives packet from device
    link drops packet
    link equeues packet
    link dequeus + sends packet
    link receives packet at other end
    router recieves packet
    router sends packet on link
    // router updates routing table...
"""

class Logger:
    """A logging class.

    Attributes:
        TO DO
    """

    def __init__(self, clock, verbose):
        self.clock = clock
        self.verbose = verbose
        self.flow_started_logs = []
        self.flow_send_packet_logs = []
        self.flow_received_acknowledgement_logs = []
        self.router_sending_packet_logs = []
        self.router_dropped_packet_unknown_path_logs = []
        self.updated_routing_table_logs = []
    
    def log_flow_started(self, flow_id):
        if self.verbose:
            print str(self.clock) + ": Flow " + str(flow_id) + " started"
        self.flow_started_logs.append({
            "time" : self.clock.current_time,
            "flow_id" : flow_id
        })

    def log_flow_send_packet(self, flow_id, packet):
        if self.verbose:
            print str(self.clock) + ": Flow " + str(flow_id) + " sending packet " + str(packet)
        self.flow_send_packet_logs.append({
            "time" : self.clock.current_time,
            "flow_id" : flow_id,
            "packet" : packet
        })

    def log_flow_received_acknowledgement(self, flow_id, packet):
        if self.verbose:
            print str(self.clock) + ": Flow " + str(flow_id) + " received acknowledgement packet " + str(packet)
        self.flow_received_acknowledgement_logs.append({
             "time" : self.clock.current_time,
             "flow_id" : flow_id,
             "packet" : packet
        })

    def log_router_sending_packet(self, router_id, packet, link_id):
        if self.verbose:
            print str(self.clock) + ": Router " + str(router_id) + " sending over link " + str(link_id) + " packet " + str(packet)
        self.router_sending_packet_logs.append({
             "time" : self.clock.current_time,
             "router_id" : router_id,
             "packet" : packet,
             "link_id" : link_id
        })

    def log_router_dropped_packet_unknown_path(self, router_id, packet):
        if self.verbose:
            print str(self.clock) + ": Router " + str(router_id) + " dropped packet because next hop is unknown: " + str(packet)
        self.router_dropped_packet_unknown_path_logs.append({
             "time" : self.clock.current_time,
             "router_id" : router_id,
             "packet" : packet
        })

    def log_updated_routing_table(self, router_id, host_id, link_id, timestamp):
        if self.verbose:
            print str(self.clock) + ": Router " + str(router_id) + " updated routing table entry for host " + str(host_id) + " to send over link " + str(link_id) + " by packet sent at time " + str(timestamp)
        self.updated_routing_table_logs.append({
             "time" : self.clock.current_time,
             "router_id" : router_id,
             "host_id" : host_id,
             "link_id" : link_id,
             "timestamp" : timestamp
        })


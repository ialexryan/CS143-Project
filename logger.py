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
        drops: (link_id, packet, time)
        flow_duration: (flow_id, duration)
        
        
        source: The host that sent the packet
        destination: The host to which the packet was sent
        packet_type: The packet type
        size: The packet size, in bytes
    """

    def __init__(self, simulation, verbose):
        self.simulation = simulation
        self.verbose = verbose
        self.flow_started_logs = []
        self.flow_send_packet_logs = []
        self.flow_received_acknowledgement_logs = []
        self.router_sending_packet_logs = []
    
    def log_flow_started(self, flow_id):
        time = self.simulation.global_time
        if self.verbose:
            print str(time / 1000) + ": Flow " + str(flow_id) + " started"
        self.flow_started_logs.append({
            "time" : time,
            "flow_id" : flow_id
        })

    def log_flow_send_packet(self, flow_id, packet):
        time = self.simulation.global_time
        if self.verbose:
            print str(time / 1000) + ": Flow " + str(flow_id) + " sending packet " + str(packet)
        self.flow_send_packet_logs.append({
            "time" : time,
            "flow_id" : flow_id,
            "packet" : packet
        })

    def log_flow_received_acknowledgement(self, flow_id, packet):
        time = self.simulation.global_time
        if self.verbose:
            print str(time / 1000) + ": Flow " + str(flow_id) + " received acknowledgement packet " + str(packet)
        self.flow_received_acknowledgement_logs.append({
             "time" : time,
             "flow_id" : flow_id,
             "packet" : packet
        })

    def log_router_sending_packet(self, router_id, packet, link_id):
        time = self.simulation.global_time
        if self.verbose:
            print str(time / 1000) + ": Router " + str(router_id) + " sending over link " + str(link_id) + " packet " + str(packet)
        self.router_sending_packet_logs.append({
             "time" : time,
             "router_id" : router_id,
             "packet" : packet,
             "link_id" : link_id
        })


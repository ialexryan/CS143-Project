import sys

class Logger:
    """Singleton class, stores arrays of log entries, which are dictionaries.
        Has methods for adding log entries to those dictionaries.
	Logs to standard output depending on verbosity."""

    def __init__(self, clock, verbose, fast_insteadof_reno):
        self.clock = clock
        self.verbose = verbose
        self.fast_insteadof_reno = fast_insteadof_reno
        self.flow_started_logs = []
        self.flow_completed_logs = []
        self.flow_send_packet_logs = []
        self.flow_received_acknowledgement_logs = []
        self.router_sending_packet_logs = []
        self.router_dropped_packet_unknown_path_logs = []
        self.updated_routing_table_logs = []
        self.link_dropped_packet_buffer_full_logs = []
        self.link_buffer_available_space_logs = []
        self.link_sent_packet_immediately_logs = []
        self.link_sent_packet_from_buffer_logs = []

    def log_flow_started(self, flow_id):
        sys.stdout.write("\r" + str(self.clock) + ": Flow " + str(flow_id) + " started              \n")
        self.flow_started_logs.append({
            "time" : self.clock.current_time,
            "flow_id" : flow_id
        })

    def log_flow_completed(self, flow_id):
        sys.stdout.write("\r" + str(self.clock) + ": Flow " + str(flow_id) + " completed            \n")
        self.flow_completed_logs.append({
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

    def log_flow_received_acknowledgement(self, flow_id, packet, amount_left):
        if self.verbose:
            print str(self.clock) + ": Flow " + str(flow_id) + " now has " +str(amount_left) + " bytes left to receive after receiving acknowledgement packet " + str(packet)
        self.flow_received_acknowledgement_logs.append({
            "time" : self.clock.current_time,
            "flow_id" : flow_id,
            "packet" : packet,
            "amount_left" : amount_left
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

    def log_link_dropped_packet_buffer_full(self, link_id, packet):
        if self.verbose:
            print str(self.clock) + ": Link " + link_id + " dropped packet because buffer is full " + str(packet)
        self.link_dropped_packet_buffer_full_logs.append({
            "time": self.clock.current_time,
            "link_id": link_id,
            "packet": packet
        })

    def log_link_buffer_available_space(self, link_id, available_space):
        self.link_buffer_available_space_logs.append({
            "time": self.clock.current_time,
            "link_id": link_id,
            "available_space": available_space
        })

    def log_link_sent_packet_immediately(self, link_id, packet):
#        print str(self.clock) + ": Link " + link_id + " sent packet immediately " + str(packet)
        self.link_sent_packet_immediately_logs.append({
            "time": self.clock.current_time,
            "link_id": link_id,
            "packet": packet
        })

    def log_link_sent_packet_from_buffer(self, link_id, packet):
#        print str(self.clock) + ": Link " + link_id + " sent packet from buffer " + str(packet)
        self.link_sent_packet_from_buffer_logs.append({
            "time": self.clock.current_time,
            "link_id": link_id,
            "packet": packet
        })

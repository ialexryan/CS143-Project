import sys
from event import FlowWakeEvent

slow_start = "Slow Start"
congestion_avoidance = "Congestion Avoidance"
fast_recovery = "Fast Recovery"

class CongestionController:
    """Implements Congestion Control

    Attributes:
        ssthresh: Slow Start Threshold
        cwnd: Congestion Window Size
        timeout: Time period after which TCP times out
        not_acknowledged: Dictionary with IDs of unacknowledged packets as key,
            and timestamp that packet was sent as value
        timed_out: List of packets whose acknowledgements haven't been received,
            and have now timed out
        duplicate_count: Counter of the number of duplicate acknowledgements
            we have received (to determine number of dropped packets)
        last_ack_received: ID of the last acknowledgement packet received
        window_start: ID of the first packet in the congestion window
        retransmit: Boolean specifying whether packets have timed out and must
            be retransmitted
        flow: Flow that the Congestion controller belongs to
        wake_event: Event specifying whether the controller should continue 
            sending packets
            
        event_scheduler: Priority queue of events to hold FlowWakeEvents
        clock: Clock for congestion controller

    """
    def __init__(self):
        self.ssthresh = 50
        self.cwnd = 1.0
        self.timeout = 1000
        self.not_acknowledged = dict()
        self.timed_out = []
        self.duplicate_count = 0
        self.last_ack_received = -1
        self.window_start = 0
        self.retransmit = False
        self.flow = None
        self.wake_event = None
        
        self.event_scheduler = None
        self.clock = None

    def acknowledgement_received(self, packet):
        sys.exit("Abstract method acknowledgement_received not implemented")

    def send_packet(self):
        sys.exit("Abstract method send_packet not implemented")
        
    def wake(self):
        sys.exit("Abstract method wake not implemented")
        
class CongestionControllerReno(CongestionController):
    """Implements TCP Reno

    Attributes:
        state: State that TCP Reno is currently in - slow start, congestion 
            avoidance, or fast recovery/fast retransmit
    """

    def __init__(self):
        CongestionController.__init__(self)
        self.state = slow_start

    def acknowledgement_received(self, packet):
        
        # Check for any unacknowledged packets that have timed out
        for packet_id in self.not_acknowledged.keys():
            sent_time = self.not_acknowledged[packet_id]
            time_diff = self.clock.current_time - sent_time
            if time_diff > self.timeout:
                del self.not_acknowledged[packet_id]
                self.timed_out.append(packet_id);
        # If we have packets that have timed out, we want to retransmit these
        if len(self.timed_out) > 0:
            self.retransmit = True
        else:
            self.retransmit = False
                
        # Remove the FlowWakeEvent from the event scheduler
        if self.wake_event != None:
            self.event_scheduler.cancel_event(self.wake_event)
            
        # Remove received packet from list of unacknowledged packets
        if packet.identifier in self.not_acknowledged.keys():
            del self.not_acknowledged[packet.identifier]
        
        # In slow start phase, increase congestion window size by 1
        if self.state == slow_start:
            self.cwnd += 1
            # If congestion window becomes larger than slow start threshold,
            # switch to congestion avoidance phase
            if self.cwnd >= self.ssthresh:
                self.state = congestion_avoidance
        elif self.state == congestion_avoidance or self.state == fast_recovery:
            # Check if this is a duplicate acknowledgement
            if packet.next_id == self.last_ack_received:
                self.duplicate_count += 1
                # After 3 duplicate acknowledgements, halve the congestion
                # window size and move into fast recovery phase
                if self.duplicate_count == 3:
                    self.cwnd /= 2
                    self.ssthresh = self.cwnd
                    self.state = fast_recovery
                    del self.not_acknowledged[packet.next_id]
            # This is not a duplicate acknowledgement
            else:
                # First non-duplicate acknowledgement in fast recovery phase
                if(self.duplicate_count >= 3):
                    self.cwnd = self.ssthresh
                    self.state = congestion_avoidance
                    self.duplicate_count = 0
                else:
                    self.cwnd += 1 / self.cwnd
        self.last_ack_received = packet.next_id
                    
        self.send_packet()        
        self.wake_event = self.event_scheduler.delay_event(self.timeout, FlowWakeEvent(self.flow))

    # Determines which packet should be sent, depending on the phase of TCP Reno            
    def send_packet(self):
        if self.state == slow_start or self.state == congestion_avoidance:
            if self.retransmit == True:
                # Retransmit timed out packets
                while (len(self.not_acknowledged) < self.cwnd) and (len(self.timed_out) > 0):
                    packet_id = self.timed_out[0]
                    self.not_acknowledged[packet_id] = self.clock.current_time
                    self.flow.send_a_packet(packet_id)
                    del self.timed_out[0]
            # Send packets, without exceeding congestion window size
            else:
                while (len(self.not_acknowledged) < self.cwnd) and (self.window_start * 1024 < self.flow.total):
                    self.not_acknowledged[self.window_start] = self.clock.current_time
                    self.flow.send_a_packet(self.window_start)
                    self.window_start += 1
        # Send dropped packet
        else:
            packet_id = self.last_ack_received
            if packet_id not in self.not_acknowledged.keys():
                self.not_acknowledged[packet_id] = self.clock.current_time
                self.flow.send_a_packet(packet_id)
    
    # Start sending packets when congestion control first begins
    def wake(self):
        # Change from fast recovery to slow start phase
        if self.state == fast_recovery:
            self.state = slow_start
        else:
            # Keep track of timed out packets
            for packet_id in self.not_acknowledged.keys():
                sent_time = self.not_acknowledged[packet_id]
                time_diff = self.clock.current_time - sent_time
                if time_diff > self.timeout:
                    del self.not_acknowledged[packet_id]
                    self.timed_out.append(packet_id);
            if len(self.timed_out) > 0:
                self.retransmit = True
            else:
                self.retransmit = False            
            self.cwnd /= 2
            self.send_packet()
        self.wake_event = None        

    def __str__(self):
        return ("ssthresh:    " + str(self.ssthresh) + "\n"
                "cwnd:        " + str(self.cwnd) + "\n"
                "duplicate ACKS" + str(self.duplicate_count) + "\n")

class CongestionControllerFast(CongestionController):
    """Implements TCP Fast

    Attributes:
        alpha:
    """

    def __init__(self):
        CongestionController.__init__(self)
        self.alpha = 10.0
        self.base_RTT = -1
        
    def acknowledgement_received(self, packet):	
        if self.wake_event != None:
            self.event_scheduler.cancel_event(self.wake_event)
        
        if self.last_ack_received == packet.next_id:
            self.duplicate_count += 1
            if self.duplicate_count == 3:
                del self.not_acknowledged[packet.next_id]
                self.timed_out.append(packet.next_id)
        else:
            self.duplicate_count = 0

        self.last_ack_received = packet.next_id

        if packet.identifier in self.not_acknowledged.keys():
            rtt = self.clock.current_time - self.not_acknowledged[packet.identifier]
            if self.base_RTT == -1:
                self.base_RTT = rtt
            
            self.cwnd = self.cwnd * self.base_RTT / rtt + self.alpha
        
            if rtt < self.base_RTT:
                self.base_RTT = rtt
            del self.not_acknowledged[packet.identifier]

        for packet_id in self.not_acknowledged.keys():
            sent_time = self.not_acknowledged[packet_id]
            time_diff = self.clock.current_time - sent_time
            if time_diff > self.timeout:
                del self.not_acknowledged[packet_id]
                self.timed_out.append(packet_id)
    
        if len(self.timed_out) > 0:
            self.retransmit = True
        else:
            self.retransmit = False

        self.send_packet()
        self.wake_event = self.event_scheduler.delay_event(self.timeout, FlowWakeEvent(self.flow))

    def send_packet(self):
        if self.retransmit == True:
            while (len(self.not_acknowledged) < self.cwnd) and (len(self.timed_out) > 0):
                packet_id = self.timed_out[0]
                self.not_acknowledged[packet_id] = self.clock.current_time
                self.flow.send_a_packet(packet_id)
                del self.timed_out[0]
        else:
            while (len(self.not_acknowledged) < self.cwnd) and (self.window_start * 1024 < self.flow.total):
                self.not_acknowledged[self.window_start] = self.clock.current_time
                self.flow.send_a_packet(self.window_start)
                self.window_start += 1

    
    def wake(self):
        for packet_id in self.not_acknowledged.keys():
            sent_time = self.not_acknowledged[packet_id]
            time_diff = self.clock.current_time - sent_time
            if time_diff > self.timeout:
                del self.not_acknowledged[packet_id]
                self.timed_out.append(packet_id);
            if len(self.timed_out) > 0:
                self.retransmit = True
            else:
                self.retransmit = False            
        self.send_packet() 
        self.wake_event = None      

    def __str__(self):
        return ("ssthresh:    " + str(self.ssthresh) + "\n"
                "cwnd:        " + str(self.cwnd) + "\n"
                "alpha:    " + str(self.alpha) + "\n")

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
        duplicate_count: Number of duplicate ACKS
    """

    def __init__(self):
        CongestionController.__init__(self)
        self.state = slow_start

    def acknowledgement_received(self, packet):
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
                
        if self.wake_event != None:
            self.event_scheduler.cancel_event(self.wake_event)
        if packet.identifier in self.not_acknowledged.keys():
            del self.not_acknowledged[packet.identifier]
            
        if self.state == slow_start:
            self.cwnd += 1
            if self.cwnd >= self.ssthresh:
                self.state = congestion_avoidance
        elif self.state == congestion_avoidance or self.state == fast_recovery:
            if packet.next_id == self.last_ack_received:
                self.duplicate_count += 1
                if self.duplicate_count == 3:
                    self.cwnd /= 2
                    self.ssthresh = self.cwnd
                    self.state = fast_recovery
                    del self.not_acknowledged[packet.next_id]
            else:
                if(self.duplicate_count >= 3):
                    self.cwnd = self.ssthresh
                    self.state = congestion_avoidance
                    self.duplicate_count = 0
                else:
                    self.cwnd += 1 / self.cwnd
        self.last_ack_received = packet.next_id
                    
        self.send_packet()        
        self.wake_event = self.event_scheduler.delay_event(self.timeout, FlowWakeEvent(self.flow))

                
    def send_packet(self):
        if self.state == slow_start or self.state == congestion_avoidance:
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
        else:
            packet_id = self.last_ack_received
            if packet_id not in self.not_acknowledged.keys():
                self.not_acknowledged[packet_id] = self.clock.current_time
                self.flow.send_a_packet(packet_id)
    
    def wake(self):
        if self.state == fast_recovery:
            self.state = slow_start
        else:
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
            self.send_packet() #TODO determine which packet to send 
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

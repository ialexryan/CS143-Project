import sys
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
        self.ssthresh = 1200
        self.cwnd = 1.0
        self.not_acknowledged = dict()
        self.flow = None

    def acknowledgement_received(self, packet):
        sys.exit("Abstract method acknowledgement_received not implemented")

    def send_packet():
        sys.exit("Abstract method send_packet not implemented")

class CongestionControllerReno(CongestionController):
    """Implements TCP Reno

    Attributes:
        duplicate_count: Number of duplicate ACKS
    """

    def __init__(self):
        CongestionController.__init__(self)
        self.duplicate_count = 0
        self.next_packet = None
        self.state = slow_start

    def acknowledgement_received(self, packet):
        if self.state == slow_start:
            cwnd += 1
            if cwnd > ssthresh:
                self.state = congestion_avoidance
        elif self.state == congestion_avoidance:
            if next_packet == packet.identifier:
                cwnd += 1 / cwnd
            else:
                duplicate_count += 1
                if duplicate_count > 3:
                    self.state = fast_recovery
                    send_packet()
        else:
            self.state = congestion_avoidance
            self.cwnd = ssthresh

    def send_packet():
        pass

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

    def acknowledgement_received(self, packet):
        pass

    def send_packet():
        pass

    def __str__(self):
        return ("ssthresh:    " + str(self.ssthresh) + "\n"
                "cwnd:        " + str(self.cwnd) + "\n"
                "alpha:    " + str(self.alpha) + "\n")

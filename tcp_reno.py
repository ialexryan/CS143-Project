from flow import Flow

class TCPReno(Flow):
    """Implements TCP Reno

    Attributes:
        ssthresh: Slow Start Threshold
        cwnd: Congestion Window Size
        duplicateCount: Number of duplicate ACKS
    """
    
    def __init__(self, identifier, source, destination, amount, start_time):
        
        Flow.__init__(self, identifier, source, destination, amount, start_time)
        self.ssthresh = 1200
        self.cwnd = 1
        self.duplicateCount = 0
    
    def __str__(self):
        return ("Flow ID      " + self.identifier + "\n"
                "source:      " + self.source.identifier + "\n"
                "destination: " + self.destination.identifier + "\n"
                "amount:      " + str(self.amount) + " bytes\n"
                "start_time:   " + str(self.start_time) + " s\n"
                "ssthresh:    " + str(self.ssthresh) + "\n"
                "cwnd:        " + str(self.cwnd) + "\n"
                "duplicate ACKS" + str(self.duplicateCount) + "\n")
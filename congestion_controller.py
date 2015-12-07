
class CongestionController:
    """Implements Congestion Control
    
    Attributes:
        ssthresh: Slow Start Threshold
        cwnd: Congestion Window Size

    """   
    def __init__(self):
        self.ssthresh = 1200
        self.cwnd = 1

class CongestionControllerReno(CongestionController):
    """Implements TCP Reno
    
    Attributes:
        duplicate_count: Number of duplicate ACKS
    """
             
    def __init__(self):
        CongestionController.__init__(self)
        self.duplicate_count = 0
    
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
    
    def __str__(self):
        return ("ssthresh:    " + str(self.ssthresh) + "\n"
                "cwnd:        " + str(self.cwnd) + "\n"
                "alpha:    " + str(self.alpha) + "\n")
        
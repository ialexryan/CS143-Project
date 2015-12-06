
class Clock:
    """A class that keeps track of the current simulation time.

    Attributes:
        current_time: the current time in simulation time, in milliseconds.
    """

    def __init__(self, time=0):
        self.current_time = time
    
    def __str__(self):
        return str(self.current_time / 1000)

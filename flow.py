class Flow:
    """A flow to be simulated on the networks

    Attributes:
        identifier: The unique identification of the flow
        souce: The source host
        destination: The destination host
        startTime: The time in which the flow simulation begins
    """

    def __init__(self, source, host, destination, startTime):
        self.identifier = identifier
        self.host = host
        self.destination = destination
        self.startTime = startTime

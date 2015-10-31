class Flow:
    """A flow to be simulated on the network

    Attributes:
        identifier: The unique identification of the flow
        source: The source host
        destination: The destination host
        amount: The amount of data to be transmitted, in MB
        startTime: The time at which the flow simulation begins, in s
    """

    def __init__(self, identifier, source, destination, amount, startTime):
        self.identifier = identifier
        self.source = source
        self.destination = destination
        self.amount = amount
        self.startTime = startTime

    def __str__(self):
        return ("Flow ID      " + self.identifier + "\n"
                "source:      " + self.source.identifier + "\n"
                "destination: " + self.destination.identifier + "\n"
                "amount:      " + str(self.amount) + " MB\n"
                "startTime:   " + str(self.startTime) + " s\n")

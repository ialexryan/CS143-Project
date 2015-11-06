from packet import PayloadPacket, AcknowledgementPacket

class Flow:
    """A flow to be simulated on the network

    Attributes:
        identifier: The unique identification of the flow
        source: The source host
        destination: The destination host
        amount: The amount of data to be transmitted, in MB
        start_time: The time at which the flow simulation begins, in s
        event_scheduler: A reference to the global event scheduler
    """

    def __init__(self, identifier, source, destination, amount, start_time):
        self.identifier = identifier
        self.source = source
        self.destination = destination
        self.amount = amount
        self.start_time = start_time
        self.event_scheduler = None

    def __str__(self):
        return ("Flow ID      " + self.identifier + "\n"
                "source:      " + self.source.identifier + "\n"
                "destination: " + self.destination.identifier + "\n"
                "amount:      " + str(self.amount) + " MB\n"
                "start_time:   " + str(self.start_time) + " s\n")

    # Called by the FlowWakeEvent to allow the flow to continue sending packets
    def wake(self):
        # NOTE THAT THIS IMPLEMENTATION IS JUST FOR TESTING
        # We need to change this to use some clever algorithm.
        packet = PayloadPacket(self.source, self.destination, 1024)
        self.source.handle_packet(packet)

    # Called by a link's host whenever an acknowledgement is recieved
    def receive_acknowledgement(self, packet):
        assert packet.source == self.destination
        assert packet.destination == self.source
        assert isinstance(packet, AcknowledgementPacket)
        print "Flow: Receiving acknowledgement"

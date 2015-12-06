from packet import PayloadPacket, AcknowledgementPacket
from congestion_control import CongestionControlReno

class Flow:
    """A flow to be simulated on the network

    Attributes:
        identifier: The unique identification of the flow
        source: The source host
        destination: The destination host
        amount: The amount of data to be transmitted, in bytes
        start_time: The time at which the flow simulation begins, in s
        event_scheduler: A reference to the global event scheduler
        complete: This flow has successfully transmitted all its data
        reno: Instance of TCP Reno.
    """

    def __init__(self, identifier, source, destination, amount, start_time):
        self.identifier = identifier
        self.source = source
        self.destination = destination
        self.amount = amount
        self.start_time = start_time
        self.event_scheduler = None
        self.logger = None
        self.complete = False
        self.reno = CongestionControlReno()

    def __str__(self):
        return ("Flow ID      " + self.identifier + "\n"
                "source:      " + self.source.identifier + "\n"
                "destination: " + self.destination.identifier + "\n"
                "amount:      " + str(self.amount) + " bytes\n"
                "start_time:   " + str(self.start_time) + " s\n")

    # Called by the FlowWakeEvent to allow the flow to continue sending packets
    def wake(self):
        self.send_a_packet()

    def send_a_packet(self):
        if (self.amount > 0):
            packet = PayloadPacket(self.source, self.destination)
            self.logger.log_flow_send_packet(self.identifier, packet)
            self.source.send_packet(packet)
        else:
            self.complete = True

    # Called by a link's host whenever an acknowledgement is received
    def acknowledgement_received(self, packet):
        assert isinstance(packet, AcknowledgementPacket)
        assert packet.source == self.destination
        assert packet.destination == self.source
        self.logger.log_flow_received_acknowledgement(self.identifier, packet)
        self.amount -= 1024 # TODO: Don't hardcode.
        self.send_a_packet()

    def completed(self):
        return self.amount is 0
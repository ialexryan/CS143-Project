from packet import PayloadPacket, AcknowledgementPacket
from congestion_controller import CongestionController

class Flow:
    """A flow to be simulated on the network

    Attributes:
        identifier: The unique identification of the flow
        source: The source host
        destination: The destination host
        amount: The amount of data to be transmitted, in bytes
        start_time: The time at which the flow simulation begins, in milliseconds
        event_scheduler: A reference to the global event scheduler
        complete: This flow has successfully transmitted all its data
        controller: Instance of Congestion Controller.
    """

    def __init__(self, identifier, source, destination, amount, start_time, controller):
        self.identifier = identifier
        self.source = source
        self.destination = destination
        self.amount = amount
        self.start_time = start_time * 1000;
        self.event_scheduler = None
        self.logger = None
        self.complete = False
        assert isinstance(controller, CongestionController)
        self.controller = controller

    def __str__(self):
        return ("Flow ID      " + self.identifier + "\n"
                "source:      " + self.source.identifier + "\n"
                "destination: " + self.destination.identifier + "\n"
                "amount:      " + str(self.amount) + " bytes\n"
                "start_time:   " + str(self.start_time) + " ms\n")

    # Called by the FlowWakeEvent to allow the flow to continue sending packets
    def wake(self):
        self.send_a_packet()

    def send_a_packet(self):
        if (self.amount > 0):
            # numbers the packets in descending order
            # packet is uniquely identified by flow and packet number
            packetID = "P" + str(self.amount / 1024) + self.identifier
            packet = PayloadPacket(packetID, self.source, self.destination)
            self.logger.log_flow_send_packet(self.identifier, packet)
            self.source.send_packet(packet)
        else:
            self.complete = True

    # Called by a link's host whenever an acknowledgement is received
    def acknowledgement_received(self, packet):
        assert isinstance(packet, AcknowledgementPacket)
        assert packet.source == self.destination
        assert packet.destination == self.source
        self.amount -= 1024 # TODO: Don't hardcode.
        self.logger.log_flow_received_acknowledgement(self.identifier, packet, self.amount)
        self.send_a_packet()

    def completed(self):
        return self.amount is 0

from packet import PayloadPacket, AcknowledgementPacket
from congestion_controller import CongestionController
from packet_tracker import PacketTracker

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
        self.total = amount
	self.done = False
        self.start_time = start_time
        self.event_scheduler = None
        self.logger = None
        self.ack_tracker = PacketTracker()
        assert isinstance(controller, CongestionController)
        self.controller = controller

    def __str__(self):
        return ("Flow ID      " + self.identifier + "\n"
                "source:      " + self.source.identifier + "\n"
                "destination: " + self.destination.identifier + "\n"
                "amount:      " + str(self.amount) + " bytes\n"
                "start_time:   " + str(self.start_time) + " ms\n")

    def set_logger(self, logger):
        self.logger = logger

    # Called by the FlowWakeEvent to allow the flow to continue sending packets
    def wake(self):
	if self.logger.clock.current_time == self.start_time:
	    self.logger.log_flow_started(self.identifier)
        self.controller.wake()

    def send_a_packet(self, packet_id, duplicate_num):
        assert(self.amount > 0)
        # numbers the packets in ascending order
        # packet is uniquely identified by flow, packet number, and which
        # duplicate of the packet it is
        packet = PayloadPacket(packet_id, duplicate_num, self.identifier, self.source, self.destination, 1024, 64)
        self.logger.log_flow_send_packet(self.identifier, packet)
        self.source.send_packet(packet)

    # Called by a link's host whenever an acknowledgement is received
    def acknowledgement_received(self, packet):
        assert isinstance(packet, AcknowledgementPacket)
        assert packet.source == self.destination
        assert packet.destination == self.source
        self.ack_tracker.account_for_packet(packet.identifier)
        self.amount = self.total - self.ack_tracker.total_count_received() * packet.payload_size
        self.logger.log_flow_received_acknowledgement(self.identifier, packet, self.amount)
        self.controller.acknowledgement_received(packet)
        if (len(self.controller.not_acknowledged) == 0) and (not self.done):
            self.logger.log_flow_completed(self.identifier)
	    self.done = True

    def completed(self):
        return self.done

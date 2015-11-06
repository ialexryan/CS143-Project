import sys
import Queue
from event import LinkWakeEvent, PacketArrivalEvent

class Buffer:
    """A buffer that holds packets that are waiting to send.

    Attributes:
        available_space: how much space in the buffer is free, in bytes
        queue: the Queue of packets waiting in the buffer
    """

    def __init__(self, size):
        self.available_space = size
        self.queue = Queue.Queue()

    def put(self, packet, destination):
        if self.available_space >= packet.size:
            self.queue.put((packet, destination))
            self.available_space -= packet.size
        # Otherwise, drop the packet

    def get(self):
        (packet, destination) = self.queue.get_nowait()
        self.available_space += packet.size
        return (packet, destination)

class Link:
    """A network link from A to B.

    Attributes:
        identifier: The unique identification of the link
        rate: The rate at which the link sends packets in bytes per second
        delay: The transmission delay between ends of the link in ms
        buffer: The Buffer storing packets
        deviceA: instance of Device
        deviceB: instance of Device
        busy: true when the link is actively transmitting
        event_schedule: reference to global event scheduler
    """

    def __init__(self, identifier, rate, delay, buffer_size, deviceA, deviceB):
        self.identifier = identifier
        self.rate = rate
        self.delay = delay
        self.buffer = Buffer(buffer_size)
        self.deviceA = deviceA
        self.deviceB = deviceB
        self.busy = False
        self.event_scheduler = None

    def __str__(self):
        return ("Link ID   " + self.identifier + "\n"
                "rate:     " + str(self.rate) + " mbps\n"
                "delay:    " + str(self.delay) + " ms\n"
                "buffer:   " + str(self.buffer.size) + " bytes\n"
                "device A: " + self.deviceA.identifier + "\n"
                "device B: " + self.deviceB.identifier) + "\n"

    # Sends a packet instantly if the link is not busy
    # or enqueues the packet in the buffer if the link is busy
    def send_packet(self, packet, sender):

        # The recipient is whatever device is not the sender
        if sender == self.deviceA:
            recipient = self.deviceB
        elif sender == self.deviceB:
            recipient = self.deviceA
        else:
            sys.exit("Sender argument of request_send_packet must be a device attached to the link")

        # Place in buffer if busy, otherwise send now
        if not self.busy:
            self._send_packet_now(packet, recipient)
        else:
            self.buffer.put(packet, recipient)

    # Called internally to send a packet by scheduling the relevant events
    def _send_packet_now(self, packet, recipient):
        assert not self.busy
        self.busy = True

        sending_delay = packet.size / self.rate
        self.event_scheduler.delay_event(sending_delay + self.delay, PacketArrivalEvent(packet, recipient))
        self.event_scheduler.delay_event(sending_delay, LinkWakeEvent(self))

    # Called by LinkWakeEvent when the link is no longer busy
    def wake(self):
        self.busy = False
        try:
            # If there are any packets in the buffer, send one
            (packet, destination) = self.buffer.get()
            self._send_packet_now(packet, destination)
        except Queue.Empty:
            pass
